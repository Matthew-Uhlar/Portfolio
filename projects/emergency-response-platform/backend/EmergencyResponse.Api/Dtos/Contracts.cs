using EmergencyResponse.Api.Models;

namespace EmergencyResponse.Api.Dtos;

public record LoginRequest(string Email, string Password);
public record LoginResponse(string Token, string Name, string Role);

public record IncidentRequest(
    string Title,
    string Description,
    string Address,
    double Latitude,
    double Longitude,
    IncidentSeverity Severity);

public record IncidentStatusRequest(IncidentStatus Status, string Note);
public record UnitRequest(string UnitName, string UnitType, string RadioCode, string CurrentLocation);
public record UnitStatusRequest(UnitStatus Status, string CurrentLocation);
public record AssignmentRequest(int IncidentId, int ResponseUnitId);
public record ActivityRequest(string Message);
