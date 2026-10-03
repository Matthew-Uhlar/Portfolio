using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.SignalR;

namespace EmergencyResponse.Api.Hubs;

[Authorize]
public class IncidentHub : Hub
{
    public Task JoinIncidentGroup(int incidentId)
    {
        return Groups.AddToGroupAsync(Context.ConnectionId, $"incident-{incidentId}");
    }

    public Task LeaveIncidentGroup(int incidentId)
    {
        return Groups.RemoveFromGroupAsync(Context.ConnectionId, $"incident-{incidentId}");
    }
}
