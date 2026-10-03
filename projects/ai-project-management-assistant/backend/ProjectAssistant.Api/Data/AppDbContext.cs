using Microsoft.EntityFrameworkCore;
using ProjectAssistant.Api.Models;

namespace ProjectAssistant.Api.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<AppUser> Users => Set<AppUser>();
    public DbSet<Project> Projects => Set<Project>();
    public DbSet<Sprint> Sprints => Set<Sprint>();
    public DbSet<WorkItem> WorkItems => Set<WorkItem>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<AppUser>().HasIndex(user => user.Email).IsUnique();

        modelBuilder.Entity<Project>()
            .HasMany(project => project.Sprints)
            .WithOne(sprint => sprint.Project)
            .HasForeignKey(sprint => sprint.ProjectId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Project>()
            .HasMany(project => project.WorkItems)
            .WithOne(item => item.Project)
            .HasForeignKey(item => item.ProjectId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Sprint>()
            .HasMany(sprint => sprint.WorkItems)
            .WithOne(item => item.Sprint)
            .HasForeignKey(item => item.SprintId)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
