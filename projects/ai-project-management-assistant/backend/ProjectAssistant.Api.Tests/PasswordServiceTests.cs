using ProjectAssistant.Api.Services;

namespace ProjectAssistant.Api.Tests;

public class PasswordServiceTests
{
    private readonly PasswordService service = new();

    [Fact]
    public void Verify_AcceptsCorrectPassword()
    {
        var stored = service.Hash("Admin123!");

        Assert.True(service.Verify("Admin123!", stored));
    }

    [Fact]
    public void Verify_RejectsWrongPassword() =>
        Assert.False(service.Verify("wrong", service.Hash("Admin123!")));

    [Fact]
    public void Hash_UsesRandomSalt() =>
        Assert.NotEqual(service.Hash("same"), service.Hash("same"));

    [Fact]
    public void Verify_RejectsMalformedHash() =>
        Assert.False(service.Verify("anything", "not-a-hash"));
}
