package com.matthewuhlar.supportflow.service;

import com.matthewuhlar.supportflow.dto.TicketDtos.UpdateTicketRequest;
import com.matthewuhlar.supportflow.model.*;
import com.matthewuhlar.supportflow.repository.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TicketRulesTest {
    @Mock TicketRepository ticketRepository;
    @Mock TicketCommentRepository commentRepository;
    @Mock TicketHistoryRepository historyRepository;
    @Mock UserRepository userRepository;
    @Mock CurrentUserService currentUserService;

    @InjectMocks TicketService ticketService;

    private final UserAccount employee = user(1L, "Erin Employee", Role.EMPLOYEE);
    private final UserAccount otherEmployee = user(2L, "Owen Other", Role.EMPLOYEE);
    private final UserAccount technician = user(3L, "Tara Tech", Role.TECHNICIAN);

    @Test
    void employeesOnlySeeTheirOwnTickets() {
        Ticket mine = ticket(10L, employee, TicketStatus.OPEN, TicketPriority.HIGH);
        Ticket mineClosed = ticket(11L, employee, TicketStatus.CLOSED, TicketPriority.LOW);
        when(currentUserService.getCurrentUser()).thenReturn(employee);
        when(ticketRepository.findByCreatedByIdOrderByCreatedAtDesc(1L)).thenReturn(List.of(mine, mineClosed));

        List<Ticket> tickets = ticketService.getTickets(TicketStatus.OPEN, null);

        assertEquals(List.of(mine), tickets);
        verify(ticketRepository, never()).findAll();
    }

    @Test
    void techniciansSeeEveryTicket() {
        Ticket a = ticket(10L, employee, TicketStatus.OPEN, TicketPriority.HIGH);
        Ticket b = ticket(11L, otherEmployee, TicketStatus.OPEN, TicketPriority.LOW);
        when(currentUserService.getCurrentUser()).thenReturn(technician);
        when(ticketRepository.findAll()).thenReturn(List.of(a, b));

        assertEquals(2, ticketService.getTickets(null, null).size());
    }

    @Test
    void employeesCannotOpenSomeoneElsesTicket() {
        when(currentUserService.getCurrentUser()).thenReturn(employee);
        when(ticketRepository.findById(20L)).thenReturn(Optional.of(ticket(20L, otherEmployee, TicketStatus.OPEN, TicketPriority.LOW)));

        assertThrows(ResourceNotFoundException.class, () -> ticketService.getTicket(20L));
    }

    @Test
    void internalNotesAreHiddenFromEmployeesButShownToTechnicians() {
        Ticket ticket = ticket(10L, employee, TicketStatus.OPEN, TicketPriority.HIGH);
        ticket.getComments().add(comment("Thanks, I restarted it", false));
        ticket.getComments().add(comment("Likely a failing power supply", true));
        when(ticketRepository.findById(10L)).thenReturn(Optional.of(ticket));

        when(currentUserService.getCurrentUser()).thenReturn(employee);
        assertEquals(1, ticketService.getTicket(10L).getVisibleComments().size());

        ticket.setHideInternalNotes(false);
        when(currentUserService.getCurrentUser()).thenReturn(technician);
        assertEquals(2, ticketService.getTicket(10L).getVisibleComments().size());
    }

    @Test
    void employeesCannotAddInternalNotes() {
        when(currentUserService.getCurrentUser()).thenReturn(employee);
        when(ticketRepository.findById(10L)).thenReturn(Optional.of(ticket(10L, employee, TicketStatus.OPEN, TicketPriority.LOW)));

        var exception = assertThrows(IllegalArgumentException.class,
            () -> ticketService.addComment(10L, "secret", true));

        assertEquals("Employees cannot add internal comments.", exception.getMessage());
        verify(commentRepository, never()).save(any());
    }

    @Test
    void ticketsCannotBeAssignedToEmployees() {
        when(currentUserService.getCurrentUser()).thenReturn(technician);
        when(ticketRepository.findById(10L)).thenReturn(Optional.of(ticket(10L, employee, TicketStatus.OPEN, TicketPriority.LOW)));
        when(userRepository.findById(2L)).thenReturn(Optional.of(otherEmployee));

        assertThrows(IllegalArgumentException.class,
            () -> ticketService.updateTicket(10L, new UpdateTicketRequest(null, null, 2L)));
    }

    @Test
    void resolvingATicketStampsResolvedAtAndRecordsHistory() {
        Ticket ticket = ticket(10L, employee, TicketStatus.IN_PROGRESS, TicketPriority.LOW);
        when(currentUserService.getCurrentUser()).thenReturn(technician);
        when(ticketRepository.findById(10L)).thenReturn(Optional.of(ticket));
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Ticket updated = ticketService.updateTicket(10L, new UpdateTicketRequest(TicketStatus.RESOLVED, null, null));

        assertEquals(TicketStatus.RESOLVED, updated.getStatus());
        assertNotNull(updated.getResolvedAt());
        assertEquals("Status changed from IN_PROGRESS to RESOLVED.", updated.getHistory().get(0).getChangeDescription());
    }

    @Test
    void assigningATicketMovesItToAssigned() {
        Ticket ticket = ticket(10L, employee, TicketStatus.OPEN, TicketPriority.LOW);
        when(currentUserService.getCurrentUser()).thenReturn(technician);
        when(ticketRepository.findById(10L)).thenReturn(Optional.of(ticket));
        when(userRepository.findById(3L)).thenReturn(Optional.of(technician));
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(invocation -> invocation.getArgument(0));

        Ticket updated = ticketService.updateTicket(10L, new UpdateTicketRequest(null, null, 3L));

        assertEquals(TicketStatus.ASSIGNED, updated.getStatus());
        assertEquals(technician, updated.getAssignedTo());
    }

    private static UserAccount user(Long id, String name, Role role) {
        UserAccount user = new UserAccount();
        user.setId(id);
        user.setName(name);
        user.setEmail(name.toLowerCase().replace(' ', '.') + "@example.com");
        user.setRole(role);
        return user;
    }

    private static Ticket ticket(Long id, UserAccount createdBy, TicketStatus status, TicketPriority priority) {
        Ticket ticket = new Ticket();
        ticket.setId(id);
        ticket.setTitle("Ticket " + id);
        ticket.setDescription("Details");
        ticket.setCreatedBy(createdBy);
        ticket.setStatus(status);
        ticket.setPriority(priority);
        return ticket;
    }

    private static TicketComment comment(String message, boolean internal) {
        TicketComment comment = new TicketComment();
        comment.setMessage(message);
        comment.setInternal(internal);
        return comment;
    }
}
