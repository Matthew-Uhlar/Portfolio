package com.matthewuhlar.supportflow.model;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
public class TicketHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Ticket ticket;

    @ManyToOne(optional = false)
    private UserAccount changedBy;

    @Column(nullable = false)
    private String changeDescription;

    @Column(nullable = false)
    private Instant createdAt = Instant.now();

    public Long getId() { return id; }
    public Ticket getTicket() { return ticket; }
    public UserAccount getChangedBy() { return changedBy; }
    public String getChangeDescription() { return changeDescription; }
    public Instant getCreatedAt() { return createdAt; }

    public void setId(Long id) { this.id = id; }
    public void setTicket(Ticket ticket) { this.ticket = ticket; }
    public void setChangedBy(UserAccount changedBy) { this.changedBy = changedBy; }
    public void setChangeDescription(String changeDescription) { this.changeDescription = changeDescription; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
