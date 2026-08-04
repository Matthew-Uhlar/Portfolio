using ProjectAssistant.Api.Models;
using ProjectAssistant.Api.Services;

namespace ProjectAssistant.Api.Data;

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
                Name = "Matthew Admin",
                Email = "admin@example.com",
                PasswordHash = passwords.Hash("Admin123!"),
                Role = UserRole.Admin
            },
            new AppUser
            {
                Name = "Demo Member",
                Email = "member@example.com",
                PasswordHash = passwords.Hash("Member123!"),
                Role = UserRole.Member
            });

        var project = new Project
        {
            Name = "Childcare Inventory Platform",
            Description = "A web application that replaces paper and spreadsheet inventory tracking.",
            Goal = "Give staff a faster way to request supplies and give administrators better visibility."
        };

        var sprint = new Sprint
        {
            Project = project,
            Name = "Sprint 3",
            Goal = "Finish the request approval workflow and improve inventory reporting.",
            StartDate = DateTime.UtcNow.Date.AddDays(-5),
            EndDate = DateTime.UtcNow.Date.AddDays(9),
            IsActive = true
        };

        db.Projects.Add(project);
        db.Sprints.Add(sprint);
        db.WorkItems.AddRange(
            new WorkItem
            {
                Project = project,
                Sprint = sprint,
                Title = "Add request approval screen",
                Description = "Administrators need a clear list of pending supply requests.",
                AcceptanceCriteria = "Admin can approve or reject a request and the change is saved.",
                Status = WorkItemStatus.InProgress,
                Priority = WorkItemPriority.High,
                StoryPoints = 5,
                Assignee = "Matthew"
            },
            new WorkItem
            {
                Project = project,
                Sprint = sprint,
                Title = "Show low stock items",
                Description = "The dashboard should highlight inventory that needs attention.",
                AcceptanceCriteria = "Items below their reorder level appear in a dashboard card.",
                Status = WorkItemStatus.Review,
                Priority = WorkItemPriority.High,
                StoryPoints = 3,
                Assignee = "Demo Member"
            },
            new WorkItem
            {
                Project = project,
                Title = "Add CSV export",
                Description = "Administrators need to download inventory data for reporting.",
                AcceptanceCriteria = "The inventory page can export the current filtered results.",
                Status = WorkItemStatus.Backlog,
                Priority = WorkItemPriority.Medium,
                StoryPoints = 3
            });

        await db.SaveChangesAsync();
    }
}
