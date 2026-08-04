using EmergencyResponse.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace EmergencyResponse.Api.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<AppUser> Users => Set<AppUser>();
    public DbSet<Incident> Incidents => Set<Incident>();
    public DbSet<ResponseUnit> ResponseUnits => Set<ResponseUnit>();
    public DbSet<IncidentAssignment> IncidentAssignments => Set<IncidentAssignment>();
    public DbSet<IncidentActivity> IncidentActivities => Set<IncidentActivity>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<AppUser>().HasIndex(user => user.Email).IsUnique();

        modelBuilder.Entity<IncidentAssignment>()
            .HasOne(assignment => assignment.Incident)
            .WithMany(incident => incident.Assignments)
            .HasForeignKey(assignment => assignment.IncidentId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<IncidentAssignment>()
            .HasOne(assignment => assignment.ResponseUnit)
            .WithMany(unit => unit.Assignments)
            .HasForeignKey(assignment => assignment.ResponseUnitId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<IncidentActivity>()
            .HasOne(activity => activity.Incident)
            .WithMany(incident => incident.Activity)
            .HasForeignKey(activity => activity.IncidentId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
