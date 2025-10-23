// lib/openapi.ts
export const openApiSpec = {
    openapi: "3.0.0",
    info: {
      title: "Citizen Services API",
      version: "1.0.0",
      description: "API para la gestión de tickets y ciudadanos. Permite crear tickets, consultar tickets por DNI y listar todos los tickets del sistema.",
      contact: {
        name: "API Support",
        email: "support@citizenservices.com"
      }
    },
    servers: [
      {
        url: "http://localhost:3000/api",
        description: "Servidor de desarrollo"
      },
      {
        url: "https://api.citizenservices.com",
        description: "Servidor de producción"
      }
    ],
    tags: [
      {
        name: "Tickets",
        description: "Operaciones relacionadas con tickets de servicio"
      }
    ],
    paths: {
      "/tickets": {
        get: {
          summary: "Listar todos los tickets",
          description: "Obtiene una lista de todos los tickets del sistema con información del ciudadano asociado",
          tags: ["Tickets"],
          responses: {
            "200": {
              description: "Lista de tickets obtenida exitosamente",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      tickets: {
                        type: "array",
                        items: {
                          $ref: "#/components/schemas/TicketWithCitizen"
                        }
                      }
                    }
                  },
                  example: {
                    tickets: [
                      {
                        id: "123e4567-e89b-12d3-a456-426614174000",
                        service: "Registro Civil",
                        status: "pending",
                        created_at: "2025-10-09T10:30:00Z",
                        citizens: {
                          dni: "1234567890",
                          first_name: "Juan",
                          last_name: "Pérez"
                        }
                      }
                    ]
                  }
                }
              }
            },
            "500": {
              description: "Error interno del servidor",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/Error"
                  }
                }
              }
            }
          }
        },
        post: {
          summary: "Crear un nuevo ticket",
          description: "Crea un ticket de servicio para un ciudadano existente identificado por su DNI",
          tags: ["Tickets"],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["dni", "service"],
                  properties: {
                    dni: {
                      type: "string",
                      description: "DNI del ciudadano",
                      example: "1234567890"
                    },
                    service: {
                      type: "string",
                      description: "Tipo de servicio solicitado",
                      example: "Registro Civil"
                    }
                  }
                }
              }
            }
          },
          responses: {
            "201": {
              description: "Ticket creado exitosamente",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      ticket: {
                        $ref: "#/components/schemas/Ticket"
                      },
                      citizen: {
                        $ref: "#/components/schemas/CitizenBasic"
                      }
                    }
                  },
                  example: {
                    ticket: {
                      id: "123e4567-e89b-12d3-a456-426614174000",
                      citizen_id: "987e6543-e21b-12d3-a456-426614174000",
                      service: "Registro Civil",
                      status: "pending",
                      created_at: "2025-10-09T10:30:00Z"
                    },
                    citizen: {
                      id: "987e6543-e21b-12d3-a456-426614174000",
                      first_name: "Juan",
                      last_name: "Pérez"
                    }
                  }
                }
              }
            },
            "400": {
              description: "Parámetros faltantes o inválidos",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/Error"
                  },
                  example: {
                    error: "Missing parameters"
                  }
                }
              }
            },
            "404": {
              description: "Ciudadano no encontrado",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/Error"
                  },
                  example: {
                    error: "Citizen not found"
                  }
                }
              }
            },
            "500": {
              description: "Error interno del servidor",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/Error"
                  }
                }
              }
            }
          }
        }
      },
      "/tickets/citizen/{dni}": {
        get: {
          summary: "Obtener tickets por DNI del ciudadano",
          description: "Busca y retorna todos los tickets asociados a un ciudadano específico identificado por su DNI",
          tags: ["Tickets"],
          parameters: [
            {
              name: "dni",
              in: "path",
              required: true,
              description: "DNI del ciudadano",
              schema: {
                type: "string",
                example: "1234567890"
              }
            }
          ],
          responses: {
            "200": {
              description: "Tickets del ciudadano obtenidos exitosamente",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      tickets: {
                        type: "array",
                        items: {
                          $ref: "#/components/schemas/Ticket"
                        }
                      }
                    }
                  },
                  example: {
                    tickets: [
                      {
                        id: "123e4567-e89b-12d3-a456-426614174000",
                        citizen_id: "987e6543-e21b-12d3-a456-426614174000",
                        service: "Registro Civil",
                        status: "pending",
                        created_at: "2025-10-09T10:30:00Z"
                      }
                    ]
                  }
                }
              }
            },
            "404": {
              description: "Ciudadano no encontrado",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/Error"
                  },
                  example: {
                    error: "Citizen not found"
                  }
                }
              }
            },
            "500": {
              description: "Error interno del servidor",
              content: {
                "application/json": {
                  schema: {
                    $ref: "#/components/schemas/Error"
                  }
                }
              }
            }
          }
        }
      }
    },
    components: {
      schemas: {
        Ticket: {
          type: "object",
          properties: {
            id: {
              type: "string",
              format: "uuid",
              description: "ID único del ticket"
            },
            citizen_id: {
              type: "string",
              format: "uuid",
              description: "ID del ciudadano asociado"
            },
            service: {
              type: "string",
              description: "Tipo de servicio solicitado"
            },
            status: {
              type: "string",
              enum: ["pending", "in_progress", "completed", "cancelled"],
              description: "Estado actual del ticket"
            },
            created_at: {
              type: "string",
              format: "date-time",
              description: "Fecha y hora de creación del ticket"
            }
          }
        },
        TicketWithCitizen: {
          type: "object",
          properties: {
            id: {
              type: "string",
              format: "uuid",
              description: "ID único del ticket"
            },
            service: {
              type: "string",
              description: "Tipo de servicio solicitado"
            },
            status: {
              type: "string",
              enum: ["pending", "in_progress", "completed", "cancelled"],
              description: "Estado actual del ticket"
            },
            created_at: {
              type: "string",
              format: "date-time",
              description: "Fecha y hora de creación del ticket"
            },
            citizens: {
              type: "object",
              properties: {
                dni: {
                  type: "string",
                  description: "DNI del ciudadano"
                },
                first_name: {
                  type: "string",
                  description: "Nombre del ciudadano"
                },
                last_name: {
                  type: "string",
                  description: "Apellido del ciudadano"
                }
              }
            }
          }
        },
        CitizenBasic: {
          type: "object",
          properties: {
            id: {
              type: "string",
              format: "uuid",
              description: "ID único del ciudadano"
            },
            first_name: {
              type: "string",
              description: "Nombre del ciudadano"
            },
            last_name: {
              type: "string",
              description: "Apellido del ciudadano"
            }
          }
        },
        Error: {
          type: "object",
          properties: {
            error: {
              type: "string",
              description: "Mensaje de error"
            }
          }
        }
      }
    }
  }