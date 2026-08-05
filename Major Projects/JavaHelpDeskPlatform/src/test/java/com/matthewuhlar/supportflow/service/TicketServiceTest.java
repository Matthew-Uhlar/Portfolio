package com.matthewuhlar.supportflow.service;

import com.matthewuhlar.supportflow.dto.TicketDtos.CreateTicketRequest;
import com.matthewuhlar.supportflow.model.*;
import com.matthewuhlar.supportflow.repository.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TicketServiceTest {
    @Mock TicketRepository ticketRepository;
    @Mock TicketCommentRepository commentRepository;
    @Mock TicketHistoryRepository historyRepository;
    @Mock UserRepository userRepository;
    @Mock CurrentUserService currentUserService;

    @InjectMocks TicketService ticketService;

    @Test
    void createTicketUsesTheSignedInUser() {
        UserAccount user = new UserAccount();
        user.setId(1L);
        user.setName("Matthew");
        user.setEmail("matthew@example.com");
        user.setRole(Role.EMPLOYEE);

        when(currentUserService.getCurrentUser()).thenReturn(user);
        when(ticketRepository.save(any(Ticket.class)))
            .thenAnswer(invocation -> invocation.getArgument(0));

        Ticket ticket = ticketService.createTicket(
            new CreateTicketRequest(
                "Printer is offline",
                "The front office printer is not responding.",
                TicketPriority.MEDIUM
            )
        );

        assertEquals("Printer is offline", ticket.getTitle());
        assertEquals(user, ticket.getCreatedBy());
        assertEquals(TicketStatus.OPEN, ticket.getStatus());
        verify(historyRepository).save(any(TicketHistory.class));
    }

    @Test
    void missingTicketReturnsAUsefulError() {
        when(ticketRepository.findById(99L)).thenReturn(java.util.Optional.empty());

        var exception = assertThrows(
            ResourceNotFoundException.class,
            () -> ticketService.getTicket(99L)
        );

        assertEquals("The ticket could not be found.", exception.getMessage());
    }
}
