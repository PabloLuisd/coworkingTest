# Trabalho Prático — Testes de Componente em um Sistema de Coworking

## Objetivo

Neste trabalho, vocês receberão um pequeno sistema de coworking já implementado, contendo:

- código-fonte do subsistema;
- testes de unidade prontos;
- estrutura básica do projeto.

O trabalho de vocês será criar os **testes de componente** do sistema, utilizando `pytest`.

Os testes de componente devem verificar a colaboração real entre as classes do subsistema, cobrindo fluxos de negócio relevantes. Não é permitido transformar o trabalho em testes unitários disfarçados, nem substituir as classes internas do subsistema por mocks.

## Sistema

O sistema representa um pequeno subsistema de reservas de salas de reunião em um espaço de coworking.

As classes principais do projeto são:

- `RoomRepository`
- `MemberRepository`
- `BookingRepository`
- `WaitlistRepository`
- `CoworkingService`

## Regras de negócio

### Reserva de sala
Um membro pode reservar uma sala somente se:

- o membro existir;
- a sala existir;
- o membro não estiver bloqueado;
- o membro não tiver mensalidade em atraso;
- a sala estiver disponível;
- o membro tiver menos de 2 reservas ativas;
- a sala não estiver na fila de espera de outro membro.

Quando a reserva é feita com sucesso:

- a sala deixa de estar disponível;
- a reserva ativa é registrada;
- se o membro tinha fila de espera para essa sala, sua entrada na fila deve ser removida.

### Liberação da sala
Ao liberar uma sala:

- a reserva ativa correspondente deve existir;
- a reserva é encerrada;
- se não houver fila de espera para a sala, ela volta a ficar disponível;
- se houver fila de espera, ela continua indisponível.

### Fila de espera
Um membro pode entrar na fila de espera de uma sala somente se:

- o membro existir;
- a sala existir;
- o membro não estiver bloqueado;
- a sala estiver indisponível;
- o membro não tiver mensalidade em atraso;
- o membro não tiver reserva duplicada para a mesma sala;
- o membro não for quem já está com a sala reservada.

A fila deve respeitar a ordem de chegada.

## Tarefa

Criem os testes de componente em:

```text
tests/components/
```

Sugestão de arquivo:

```text
tests/components/test_coworking_component.py
```

## Quantidade esperada
Espera-se entre **10 e 12 testes de componente**.

## Cenários mínimos obrigatórios

1. reserva com sucesso;
2. reserva de sala inexistente;
3. reserva por membro inexistente;
4. reserva bloqueada por mensalidade em atraso;
5. reserva bloqueada por membro bloqueado;
6. reserva bloqueada por limite de 2 reservas ativas;
7. entrada na fila de espera com sucesso para sala indisponível;
8. tentativa de fila duplicada;
9. liberação simples sem fila de espera;
10. liberação com fila de espera, mantendo a sala indisponível;
11. reserva bem-sucedida por membro que tinha fila de espera para a mesma sala, removendo a fila;
12. sequência completa: reserva → fila de espera por outro membro → liberação → tentativa de nova reserva.

## Requisitos de qualidade

Os testes devem:

- usar as classes reais do subsistema;
- refletir fluxos de negócio;
- ser legíveis e bem nomeados;
- evitar duplicação excessiva;
- ser determinísticos.

## Execução

Para executar os testes de unidade:

```bash
pytest tests/unit
```

Para executar todos os testes:

```bash
pytest
```
