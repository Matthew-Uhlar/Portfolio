package com.matthewuhlar.supportflow.dto;

import com.matthewuhlar.supportflow.model.TicketPriority;
import com.matthewuhlar.supportflow.model.TicketStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public final class TicketDtos {
    private TicketDtos() {}

    public record CreateTicketRequest(
        @NotBlank String title,
        @NotBlank String description,
        @NotNull TicketPriority priority
    ) {}

    public record UpdateTicketRequest(
        TicketStatus status,
        TicketPriority priority,
        Long assignedToUserId
    ) {}

    public record CommentRequest(
        @NotBlank String message,
        boolean internal
    ) {}
}
