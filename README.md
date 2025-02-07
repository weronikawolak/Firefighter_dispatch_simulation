# Firefighter_dispatch_simulation
This project simulates the dispatching of firefighting units in the city of Kraków. The simulation models emergency response scenarios where fire stations deploy vehicles based on event types and geographical locations. The project applies fundamental software design principles (SOLID) and utilizes behavioral design patterns to ensure modularity and scalability. 


## Implemented Design Patterns
- **Strategy** – Allows switching between different dispatching strategies dynamically.
- **Observer** – Implements a notification system to inform units about emergency events.
- **State** – Tracks and manages the status of vehicles (**available, dispatched, busy**).
- **Iterator** – Provides controlled sequential access to firefighting units.

### Fire Stations
- 7 main **JRG** units.
- Additional specialized units: **ASP, Skawina, Airport.**

### Vehicles
- Each unit has **5 fire trucks**, which respond to incidents.

### Incident Types
- **Fire (PZ)** – Requires **3 trucks**.
- **False Alarm (AF)** – No action needed, but verification is required.
- **Local Threat (MZ)** – Requires **2 trucks**.

### Dispatching Logic
- Vehicles from the **nearest available station** respond first.
- If a station has no available trucks, the **next nearest station** provides support.
- Response times and outcomes are **randomized**:
  - **False alarms** (5% probability).
  - **Random travel times** (**0-3s**).
  - **Action duration** (**5-25s**) before returning to base.

