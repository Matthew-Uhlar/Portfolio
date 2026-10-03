using System.Text;
using Inventory.Api.Data;
using Inventory.Api.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;

var builder=WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>(o=>o.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddScoped<TokenService>();
builder.Services.AddControllers().AddJsonOptions(o=>o.JsonSerializerOptions.Converters.Add(new System.Text.Json.Serialization.JsonStringEnumConverter()));
builder.Services.AddCors(o=>o.AddDefaultPolicy(p=>p.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer(o=>{o.TokenValidationParameters=new TokenValidationParameters{ValidateIssuer=true,ValidateAudience=true,ValidateLifetime=true,ValidateIssuerSigningKey=true,ValidIssuer=builder.Configuration["Jwt:Issuer"],ValidAudience=builder.Configuration["Jwt:Audience"],IssuerSigningKey=new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))};});
builder.Services.AddAuthorization();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c=>{c.SwaggerDoc("v1",new OpenApiInfo{Title="Inventory API",Version="v1"});c.AddSecurityDefinition("Bearer",new OpenApiSecurityScheme{Type=SecuritySchemeType.Http,Scheme="bearer",BearerFormat="JWT"});c.AddSecurityRequirement(new OpenApiSecurityRequirement{{new OpenApiSecurityScheme{Reference=new OpenApiReference{Type=ReferenceType.SecurityScheme,Id="Bearer"}},Array.Empty<string>()}});});
var app=builder.Build();app.UseSwagger();app.UseSwaggerUI();app.UseCors();app.UseAuthentication();app.UseAuthorization();app.MapControllers();
using(var scope=app.Services.CreateScope()){var db=scope.ServiceProvider.GetRequiredService<AppDbContext>();await DbSeeder.SeedAsync(db);}app.Run();
