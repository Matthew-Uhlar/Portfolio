using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Data;
using ProjectAssistant.Api.Dtos;
using ProjectAssistant.Api.Services;

namespace ProjectAssistant.Api.Controllers;

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
