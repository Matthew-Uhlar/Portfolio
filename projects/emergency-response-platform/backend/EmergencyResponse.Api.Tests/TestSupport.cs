using System.Security.Claims;
using EmergencyResponse.Api.Data;
using EmergencyResponse.Api.Hubs;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;

namespace EmergencyResponse.Api.Tests;

/// <summary>Shared helpers: an isolated in-memory database and a hub that records broadcasts.</summary>
internal static class TestSupport
{
    public static AppDbContext CreateDb() =>
        new(new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options);

    public static T SignedInAs<T>(this T controller, string name) where T : ControllerBase
    {
        var identity = new ClaimsIdentity(new[] { new Claim(ClaimTypes.Name, name) }, "Test");
        controller.ControllerContext = new ControllerContext
        {
            HttpContext = new DefaultHttpContext { User = new ClaimsPrincipal(identity) }
        };
        return controller;
    }
}

/// <summary>Captures every SignalR message the controllers send so tests can assert on them.</summary>
internal sealed class RecordingHub : IHubContext<IncidentHub>
{
    private readonly RecordingClients clients = new();

    public List<(string Target, string Method, object?[] Args)> Sent => clients.Sent;
    public IHubClients Clients => clients;
    public IGroupManager Groups => throw new NotSupportedException();

    private sealed class RecordingClients : IHubClients
    {
        public List<(string Target, string Method, object?[] Args)> Sent { get; } = [];

        public IClientProxy All => Proxy("All");
        public IClientProxy AllExcept(IReadOnlyList<string> excludedConnectionIds) => Proxy("AllExcept");
        public IClientProxy Client(string connectionId) => Proxy($"client:{connectionId}");
        public IClientProxy Clients(IReadOnlyList<string> connectionIds) => Proxy("clients");
        public IClientProxy Group(string groupName) => Proxy($"group:{groupName}");
        public IClientProxy GroupExcept(string groupName, IReadOnlyList<string> excludedConnectionIds) => Proxy($"group:{groupName}");
        public IClientProxy Groups(IReadOnlyList<string> groupNames) => Proxy("groups");
        public IClientProxy User(string userId) => Proxy($"user:{userId}");
        public IClientProxy Users(IReadOnlyList<string> userIds) => Proxy("users");

        private RecordingProxy Proxy(string target) => new(target, Sent);
    }

    private sealed class RecordingProxy(string target, List<(string, string, object?[])> sent) : IClientProxy
    {
        public Task SendCoreAsync(string method, object?[] args, CancellationToken cancellationToken = default)
        {
            sent.Add((target, method, args));
            return Task.CompletedTask;
        }
    }
}
