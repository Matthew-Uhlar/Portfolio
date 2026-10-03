using EmergencyResponse.Api.Models;
using EmergencyResponse.Api.Services;

namespace EmergencyResponse.Api.Data;

public static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, PasswordService passwords)
    {
        if (db.Users.Any())
        {
            return;
        }

        db.Users.AddRange(
            new AppUser
            {
                Name = "Matthew Dispatcher",
                Email = "dispatcher@example.com",
                PasswordHash = passwords.Hash("Dispatch123!"),
                Role = UserRole.Dispatcher
            },
            new AppUser
            {
                Name = "Demo Responder",
                Email = "responder@example.com",
                PasswordHash = passwords.Hash("Responder123!"),
                Role = UserRole.Responder
            });

        var fireUnit = new ResponseUnit
        {
            UnitName = "Engine 12",
            UnitType = "Fire Engine",
            RadioCode = "E12",
            Status = UnitStatus.Assigned,
            CurrentLocation = "East Austin"
        };

        var utilityUnit = new ResponseUnit
        {
            UnitName = "Utility 4",
            UnitType = "Infrastructure Response",
            RadioCode = "U4",
            Status = UnitStatus.Available,
            CurrentLocation = "Downtown Austin"
        };

        var medicalUnit = new ResponseUnit
        {
            UnitName = "Medic 7",
            UnitType = "Ambulance",
            RadioCode = "M7",
            Status = UnitStatus.Available,
            CurrentLocation = "South Austin"
        };

        var incident = new Incident
        {
            Title = "Power line down near roadway",
            Description = "A damaged utility pole left a live line close to traffic.",
            Address = "2200 Riverside Drive, Austin, TX",
            Latitude = 30.2397,
            Longitude = -97.7274,
            Severity = IncidentSeverity.High,
            Status = IncidentStatus.Dispatched
        };

        db.ResponseUnits.AddRange(fireUnit, utilityUnit, medicalUnit);
        db.Incidents.Add(incident);

        db.IncidentAssignments.Add(new IncidentAssignment
        {
            Incident = incident,
            ResponseUnit = fireUnit
        });

        db.IncidentActivities.AddRange(
            new IncidentActivity
            {
                Incident = incident,
                Message = "Incident was reported by a field supervisor.",
                CreatedBy = "Matthew Dispatcher"
            },
            new IncidentActivity
            {
                Incident = incident,
                Message = "Engine 12 was assigned to secure the area.",
                CreatedBy = "Matthew Dispatcher"
            });

        await db.SaveChangesAsync();
    }
}
