# Initial architecture

Cynlith uses a monorepo with independently owned packages.

- `frontend/` is the user-facing Expo/React application.
- `backend/` is the FastAPI HTTP service boundary.
- `ai/` will hold AI-specific implementation only after its scope is defined.
- `firmware/` will hold device-specific implementation only after hardware scope is defined.

Packages communicate through explicit, documented interfaces. The foundation intentionally defines no product integrations or persistent services.
