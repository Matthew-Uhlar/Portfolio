namespace EmergencyResponse.Api.Models;

public enum UserRole
{
    Dispatcher,
    Responder
}

public enum IncidentStatus
{
    Reported,
    Dispatched,
    OnScene,
    Contained,
    Closed
}

public enum IncidentSeverity
{
    Low,
    Moderate,
    High,
    Critical
}

public enum UnitStatus
{
    Available,
    Assigned,
    EnRoute,
    OnScene,
    Unavailable
}

public class AppUser
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string PasswordHash { get; set; } = "";
    public UserRole Role { get; set; }
}

public class Incident
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    public string Address { get; set; } = "";
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public IncidentStatus Status { get; set; } = IncidentStatus.Reported;
    public IncidentSeverity Severity { get; set; } = IncidentSeverity.Moderate;
    public DateTime ReportedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ClosedAt { get; set; }
    public List<IncidentAssignment> Assignments { get; set; } = [];
    public List<IncidentActivity> Activity { get; set; } = [];
}

public class ResponseUnit
{
    public int Id { get; set; }
    public string UnitName { get; set; } = "";
    public string UnitType { get; set; } = "";
    public string RadioCode { get; set; } = "";
    public UnitStatus Status { get; set; } = UnitStatus.Available;
    public string CurrentLocation { get; set; } = "";
    public List<IncidentAssignment> Assignments { get; set; } = [];
}

public class IncidentAssignment
{
    public int Id { get; set; }
    public int IncidentId { get; set; }
    public Incident? Incident { get; set; }
    public int ResponseUnitId { get; set; }
    public ResponseUnit? ResponseUnit { get; set; }
    public DateTime AssignedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ClearedAt { get; set; }
}

public class IncidentActivity
{
    public int Id { get; set; }
    public int IncidentId { get; set; }
    public Incident? Incident { get; set; }
    public string Message { get; set; } = "";
    public string CreatedBy { get; set; } = "";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
