package com.matthewuhlar.supportflow.model;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
public class TicketComment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Ticket ticket;

    @ManyToOne(optional = false)
    private UserAccount author;

    @Column(nullable = false, length = 2000)
    private String message;

    @Column(nullable = false)
    private boolean internal;

    @Column(nullable = false)
    private Instant createdAt = Instant.now();

    public Long getId() { return id; }
    public Ticket getTicket() { return ticket; }
    public UserAccount getAuthor() { return author; }
    public String getMessage() { return message; }
    public boolean isInternal() { return internal; }
    public Instant getCreatedAt() { return createdAt; }

    public void setId(Long id) { this.id = id; }
    public void setTicket(Ticket ticket) { this.ticket = ticket; }
    public void setAuthor(UserAccount author) { this.author = author; }
    public void setMessage(String message) { this.message = message; }
    public void setInternal(boolean internal) { this.internal = internal; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
