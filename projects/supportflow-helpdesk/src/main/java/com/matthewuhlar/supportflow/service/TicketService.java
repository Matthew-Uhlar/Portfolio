package com.matthewuhlar.supportflow.service;

import com.matthewuhlar.supportflow.dto.TicketDtos.CreateTicketRequest;
import com.matthewuhlar.supportflow.dto.TicketDtos.UpdateTicketRequest;
import com.matthewuhlar.supportflow.model.*;
import com.matthewuhlar.supportflow.repository.*;
import org.hibernate.Hibernate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Service
public class TicketService {
    private final TicketRepository ticketRepository;
    private final TicketCommentRepository commentRepository;
    private final TicketHistoryRepository historyRepository;
    private final UserRepository userRepository;
    private final CurrentUserService currentUserService;

    public TicketService(
        TicketRepository ticketRepository,
        TicketCommentRepository commentRepository,
        TicketHistoryRepository historyRepository,
        UserRepository userRepository,
        CurrentUserService currentUserService
    ) {
        this.ticketRepository = ticketRepository;
        this.commentRepository = commentRepository;
        this.historyRepository = historyRepository;
        this.userRepository = userRepository;
        this.currentUserService = currentUserService;
    }

    @Transactional(readOnly = true)
    public List<Ticket> getTickets(TicketStatus status, TicketPriority priority) {
        List<Ticket> tickets;

        if (status != null) {
            tickets = ticketRepository.findByStatusOrderByCreatedAtDesc(status);
        } else if (priority != null) {
            tickets = ticketRepository.findByPriorityOrderByCreatedAtDesc(priority);
        } else {
            tickets = ticketRepository.findAll();
        }

        tickets.forEach(this::loadDetails);
        return tickets;
    }

    @Transactional(readOnly = true)
    public Ticket getTicket(long id) {
        Ticket ticket = ticketRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("The ticket could not be found."));
        loadDetails(ticket);
        return ticket;
    }

    // Responses are serialized after the transaction closes (open-in-view is off),
    // so load the comment and history collections while the session is still open.
    private void loadDetails(Ticket ticket) {
        Hibernate.initialize(ticket.getComments());
        Hibernate.initialize(ticket.getHistory());
    }

    @Transactional
    public Ticket createTicket(CreateTicketRequest request) {
        UserAccount user = currentUserService.getCurrentUser();

        Ticket ticket = new Ticket();
        ticket.setTitle(request.title().trim());
        ticket.setDescription(request.description().trim());
        ticket.setPriority(request.priority());
        ticket.setCreatedBy(user);

        Ticket saved = ticketRepository.save(ticket);
        addHistory(saved, user, "Ticket was created.");

        return saved;
    }

    @Transactional
    public Ticket updateTicket(long id, UpdateTicketRequest request) {
        Ticket ticket = getTicket(id);
        UserAccount user = currentUserService.getCurrentUser();

        if (request.status() != null && request.status() != ticket.getStatus()) {
            TicketStatus oldStatus = ticket.getStatus();
            ticket.setStatus(request.status());

            if (request.status() == TicketStatus.RESOLVED || request.status() == TicketStatus.CLOSED) {
                ticket.setResolvedAt(Instant.now());
            }

            addHistory(ticket, user, "Status changed from " + oldStatus + " to " + request.status() + ".");
        }

        if (request.priority() != null && request.priority() != ticket.getPriority()) {
            TicketPriority oldPriority = ticket.getPriority();
            ticket.setPriority(request.priority());
            addHistory(ticket, user, "Priority changed from " + oldPriority + " to " + request.priority() + ".");
        }

        if (request.assignedToUserId() != null) {
            UserAccount technician = userRepository.findById(request.assignedToUserId())
                .orElseThrow(() -> new ResourceNotFoundException("The assigned user could not be found."));

            if (technician.getRole() == Role.EMPLOYEE) {
                throw new IllegalArgumentException("Tickets can only be assigned to technicians or administrators.");
            }

            ticket.setAssignedTo(technician);
            ticket.setStatus(TicketStatus.ASSIGNED);
            addHistory(ticket, user, "Ticket was assigned to " + technician.getName() + ".");
        }

        ticket.setUpdatedAt(Instant.now());
        return ticketRepository.save(ticket);
    }

    @Transactional
    public TicketComment addComment(long ticketId, String message, boolean internal) {
        Ticket ticket = getTicket(ticketId);
        UserAccount user = currentUserService.getCurrentUser();

        if (internal && user.getRole() == Role.EMPLOYEE) {
            throw new IllegalArgumentException("Employees cannot add internal comments.");
        }

        TicketComment comment = new TicketComment();
        comment.setTicket(ticket);
        comment.setAuthor(user);
        comment.setMessage(message.trim());
        comment.setInternal(internal);

        addHistory(ticket, user, internal ? "An internal note was added." : "A comment was added.");
        return commentRepository.save(comment);
    }

    private void addHistory(Ticket ticket, UserAccount user, String description) {
        TicketHistory history = new TicketHistory();
        history.setTicket(ticket);
        history.setChangedBy(user);
        history.setChangeDescription(description);
        historyRepository.save(history);
        if (ticket != null) {
            ticket.getHistory().add(0, history);
        }
    }
}
