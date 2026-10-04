using EmergencyResponse.Api.Controllers;
using EmergencyResponse.Api.Dtos;
using EmergencyResponse.Api.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EmergencyResponse.Api.Tests;

public class IncidentAndAssignmentTests
{
    [Fact]
    public async Task CreateIncident_TrimsInputLogsActivityAndBroadcasts()
    {
        using var db = TestSupport.CreateDb();
        var hub = new RecordingHub();
        var controller = new IncidentsController(db, hub).SignedInAs("Dana Dispatcher");

        var result = await controller.Create(new IncidentRequest("  House fire ", " Smoke visible ", " 12 Main St ", 30.26, -97.74, IncidentSeverity.Critical));

        var created = Assert.IsType<CreatedAtActionResult>(result.Result);
        var incident = Assert.IsType<Incident>(created.Value);
        Assert.Equal("House fire", incident.Title);
        Assert.Equal("12 Main St", incident.Address);
        Assert.Equal(IncidentStatus.Reported, incident.Status);

        var activity = await db.IncidentActivities.SingleAsync();
        Assert.Equal("Incident was created.", activity.Message);
        Assert.Equal("Dana Dispatcher", activity.CreatedBy);
        Assert.Contains(hub.Sent, message => message.Target == "All" && message.Method == "IncidentCreated");
    }

    [Fact]
    public async Task ClosingAnIncident_SetsClosedAtAndReopeningClearsIt()
    {
        using var db = TestSupport.CreateDb();
        db.Incidents.Add(new Incident { Id = 1, Title = "Crash" });
        await db.SaveChangesAsync();
        var controller = new IncidentsController(db, new RecordingHub()).SignedInAs("Dana");

        await controller.UpdateStatus(1, new IncidentStatusRequest(IncidentStatus.Closed, ""));
        Assert.NotNull((await db.Incidents.FindAsync(1))!.ClosedAt);

        await controller.UpdateStatus(1, new IncidentStatusRequest(IncidentStatus.OnScene, "Re-opened after new call"));
        var incident = await db.Incidents.FindAsync(1);
        Assert.Null(incident!.ClosedAt);

        var notes = await db.IncidentActivities.OrderBy(item => item.Id).Select(item => item.Message).ToListAsync();
        Assert.Equal(new[] { "Status changed to Closed.", "Re-opened after new call" }, notes);
    }

    [Fact]
    public async Task UpdateStatus_UnknownIncident_ReturnsNotFound()
    {
        using var db = TestSupport.CreateDb();
        var controller = new IncidentsController(db, new RecordingHub()).SignedInAs("Dana");

        var result = await controller.UpdateStatus(99, new IncidentStatusRequest(IncidentStatus.Closed, ""));

        Assert.IsType<NotFoundResult>(result.Result);
    }

    [Fact]
    public async Task AddNote_BroadcastsOnlyToThatIncidentsGroup()
    {
        using var db = TestSupport.CreateDb();
        db.Incidents.Add(new Incident { Id = 5, Title = "Flood" });
        await db.SaveChangesAsync();
        var hub = new RecordingHub();

        await new IncidentsController(db, hub).SignedInAs("Dana").AddNote(5, new ActivityRequest(" Water rising "));

        var sent = Assert.Single(hub.Sent);
        Assert.Equal("group:incident-5", sent.Target);
        Assert.Equal("ActivityAdded", sent.Method);
        Assert.Equal("Water rising", (await db.IncidentActivities.SingleAsync()).Message);
    }

    [Fact]
    public async Task Assign_MarksUnitAssignedAndDispatchesReportedIncident()
    {
        using var db = Seed();
        var hub = new RecordingHub();

        var result = await new AssignmentsController(db, hub).SignedInAs("Dana").Assign(new AssignmentRequest(1, 1));

        Assert.IsType<OkObjectResult>(result.Result);
        Assert.Equal(UnitStatus.Assigned, (await db.ResponseUnits.FindAsync(1))!.Status);
        Assert.Equal(IncidentStatus.Dispatched, (await db.Incidents.FindAsync(1))!.Status);
        Assert.Equal("Engine 7 was assigned.", (await db.IncidentActivities.SingleAsync()).Message);
        Assert.Contains(hub.Sent, message => message.Method == "AssignmentCreated");
    }

    [Fact]
    public async Task Assign_DoesNotDowngradeAnIncidentAlreadyOnScene()
    {
        using var db = Seed(IncidentStatus.OnScene);

        await new AssignmentsController(db, new RecordingHub()).SignedInAs("Dana").Assign(new AssignmentRequest(1, 1));

        Assert.Equal(IncidentStatus.OnScene, (await db.Incidents.FindAsync(1))!.Status);
    }

    [Fact]
    public async Task Assign_SameUnitTwice_IsRejected()
    {
        using var db = Seed();
        var controller = new AssignmentsController(db, new RecordingHub()).SignedInAs("Dana");

        await controller.Assign(new AssignmentRequest(1, 1));
        var second = await controller.Assign(new AssignmentRequest(1, 1));

        Assert.IsType<BadRequestObjectResult>(second.Result);
        Assert.Equal(1, await db.IncidentAssignments.CountAsync());
    }

    [Fact]
    public async Task Assign_UnknownUnit_ReturnsNotFound()
    {
        using var db = Seed();

        var result = await new AssignmentsController(db, new RecordingHub()).SignedInAs("Dana").Assign(new AssignmentRequest(1, 42));

        Assert.IsType<NotFoundObjectResult>(result.Result);
    }

    [Fact]
    public async Task Clear_FreesTheUnitAndAllowsReassignment()
    {
        using var db = Seed();
        var hub = new RecordingHub();
        var controller = new AssignmentsController(db, hub).SignedInAs("Dana");
        await controller.Assign(new AssignmentRequest(1, 1));
        var assignmentId = (await db.IncidentAssignments.SingleAsync()).Id;

        var cleared = await controller.Clear(assignmentId);

        Assert.IsType<NoContentResult>(cleared);
        Assert.Equal(UnitStatus.Available, (await db.ResponseUnits.FindAsync(1))!.Status);
        Assert.NotNull((await db.IncidentAssignments.FindAsync(assignmentId))!.ClearedAt);
        Assert.Contains(hub.Sent, message => message.Method == "AssignmentCleared");

        var again = await controller.Assign(new AssignmentRequest(1, 1));
        Assert.IsType<OkObjectResult>(again.Result);
    }

    private static Data.AppDbContext Seed(IncidentStatus status = IncidentStatus.Reported)
    {
        var db = TestSupport.CreateDb();
        db.Incidents.Add(new Incident { Id = 1, Title = "House fire", Status = status });
        db.ResponseUnits.Add(new ResponseUnit { Id = 1, UnitName = "Engine 7" });
        db.SaveChanges();
        return db;
    }
}
