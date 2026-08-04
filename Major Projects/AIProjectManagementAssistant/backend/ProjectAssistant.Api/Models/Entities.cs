namespace ProjectAssistant.Api.Models;

public enum UserRole
{
    Admin,
    Member
}

public enum WorkItemStatus
{
    Backlog,
    Ready,
    InProgress,
    Review,
    Done
}

public enum WorkItemPriority
{
    Low,
    Medium,
    High,
    Critical
}

public class AppUser
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string PasswordHash { get; set; } = "";
    public UserRole Role { get; set; } = UserRole.Member;
}

public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public string Goal { get; set; } = "";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public List<Sprint> Sprints { get; set; } = [];
    public List<WorkItem> WorkItems { get; set; } = [];
}

public class Sprint
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public Project? Project { get; set; }
    public string Name { get; set; } = "";
    public string Goal { get; set; } = "";
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public bool IsActive { get; set; }
    public List<WorkItem> WorkItems { get; set; } = [];
}

public class WorkItem
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public Project? Project { get; set; }
    public int? SprintId { get; set; }
    public Sprint? Sprint { get; set; }
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    public string AcceptanceCriteria { get; set; } = "";
    public WorkItemStatus Status { get; set; } = WorkItemStatus.Backlog;
    public WorkItemPriority Priority { get; set; } = WorkItemPriority.Medium;
    public int StoryPoints { get; set; } = 3;
    public string Assignee { get; set; } = "";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
