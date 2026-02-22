# Frontend Structure

## 📁 Directory Organization

```
src/
├── api/              # API clients and endpoints
│   ├── client.ts     # Axios instance
│   ├── auth.ts       # Authentication API
│   ├── rooms.ts      # Rooms API
│   ├── bookings.ts   # Bookings API
│   └── index.ts      # API exports
│
├── assets/           # Static assets (images, fonts)
│
├── components/       # Reusable components
│   ├── smart/        # Smart/connected components
│   │   ├── BookingWidget.vue
│   │   ├── ChatBubble.vue
│   │   └── LiveCounter.vue
│   └── OptimizedImage.vue
│
├── composables/      # Vue composables
│   └── useAuth.ts
│
├── i18n/             # Internationalization
│   ├── index.ts
│   └── locales/
│       ├── ar.json
│       └── en.json
│
├── pages/            # Main page components
│   ├── HomePage.vue
│   ├── RoomsPage.vue
│   ├── RoomDetailPage.vue
│   └── BeachPage.vue
│
├── router/           # Vue Router configuration
│   └── index.ts
│
├── stores/           # Pinia stores
│   ├── auth.ts
│   └── booking.ts
│
├── types/            # TypeScript types
│   └── index.ts
│
├── views/            # View components (auth, account)
│   ├── LoginView.vue
│   ├── RegisterView.vue
│   ├── AccountView.vue
│   └── BookingView.vue
│
├── App.vue           # Root component
├── main.ts           # App entry point
└── style.css         # Global styles (Tailwind)
```

## 🎯 Component Categories

### Pages (`/pages`)
Full-page components for main routes:
- `HomePage.vue` - Landing page with hero, services, packages
- `RoomsPage.vue` - Room listing with filters
- `RoomDetailPage.vue` - Individual room details
- `BeachPage.vue` - Beach services and booking

### Views (`/views`)
Smaller view components for specific features:
- `LoginView.vue` - User login
- `RegisterView.vue` - User registration
- `AccountView.vue` - User account management
- `BookingView.vue` - Booking management

### Components (`/components`)
Reusable UI components:
- `OptimizedImage.vue` - Image optimization wrapper
- `smart/BookingWidget.vue` - Quick booking widget
- `smart/ChatBubble.vue` - AI chatbot interface
- `smart/LiveCounter.vue` - Real-time viewer counter

## 🎨 Styling

- **Framework**: Tailwind CSS v4
- **Custom Colors**: 
  - `ocean-deep` (50-900)
  - `teal-glow` (50-900)
- **Fonts**: Inter (English), Cairo (Arabic)
- **Responsive**: Mobile-first design

## 🔧 Key Features

1. **Authentication**: JWT-based auth with Pinia store
2. **Internationalization**: Arabic/English support
3. **Real-time**: Live counters and chat
4. **Responsive**: All screen sizes supported
5. **Type-safe**: Full TypeScript support

## 📝 Naming Conventions

- **Components**: PascalCase (e.g., `BookingWidget.vue`)
- **Files**: camelCase for TS/JS (e.g., `useAuth.ts`)
- **Routes**: kebab-case (e.g., `/room-detail`)
- **CSS Classes**: Tailwind utilities + custom classes

## 🚀 Development

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```
