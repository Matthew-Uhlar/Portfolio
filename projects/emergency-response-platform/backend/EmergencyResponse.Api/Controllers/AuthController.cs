using EmergencyResponse.Api.Data;
using EmergencyResponse.Api.Dtos;
using EmergencyResponse.Api.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EmergencyResponse.Api.Controllers;

[ApiController]
[Route("api/auth")]
public class AuthController(AppDbContext db, PasswordService passwords, TokenService tokens) : ControllerBase
{
    [HttpPost("login")]
    public async Task<ActionResult<LoginResponse>> Login(LoginRequest request)
    {
        var email = request.Email.Trim().ToLowerInvariant();
        var user = await db.Users.SingleOrDefaultAsync(item => item.Email == email);

        if (user is null || !passwords.Verify(request.Password, user.PasswordHash))
        {
            return Unauthorized(new { message = "The email or password was not correct." });
        }

        return Ok(new LoginResponse(tokens.Create(user), user.Name, user.Role.ToString()));
    }
}
