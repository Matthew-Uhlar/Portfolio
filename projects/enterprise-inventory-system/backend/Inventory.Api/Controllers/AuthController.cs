using Inventory.Api.Data;
using Inventory.Api.Dtos;
using Inventory.Api.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Inventory.Api.Controllers;

[ApiController, Route("api/auth")]
public class AuthController(AppDbContext db, TokenService tokens) : ControllerBase
{
    [HttpPost("login")]
    public async Task<ActionResult<LoginResponse>> Login(LoginRequest request)
    {
        var user = await db.Users.SingleOrDefaultAsync(x => x.Email == request.Email.ToLower());
        if (user is null || !PasswordService.Verify(request.Password, user.PasswordHash)) return Unauthorized(new { message = "Invalid email or password." });
        return new LoginResponse(tokens.Create(user), user.Name, user.Role.ToString());
    }
}
