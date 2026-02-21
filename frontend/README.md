# الخيمة Beach Resort - Frontend

Modern, responsive Vue 3 + TypeScript frontend for a luxury beach resort booking system.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🛠️ Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Animations**: GSAP
- **i18n**: Vue I18n (Arabic/English)

## 📁 Project Structure

```
src/
├── api/              # API clients and endpoints
├── components/       # Reusable UI components
│   ├── Navbar.vue    # Global navigation
│   ├── Footer.vue    # Global footer
│   └── smart/        # Smart/connected components
├── pages/            # Main page components
├── views/            # Auth & account views
├── stores/           # Pinia state stores
├── router/           # Vue Router config
├── i18n/             # Internationalization
└── types/            # TypeScript definitions
```

See [STRUCTURE.md](./STRUCTURE.md) for detailed documentation.

## 🎨 Features

- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Dark/light mode ready
- ✅ Arabic/English support
- ✅ Real-time booking updates
- ✅ AI chatbot integration
- ✅ Optimized images
- ✅ SEO friendly
- ✅ Type-safe with TypeScript

## 🎯 Key Pages

- **Home** (`/`) - Hero, services, packages, testimonials
- **Rooms** (`/rooms`) - Room listing with live counters
- **Room Detail** (`/rooms/:id`) - Individual room details
- **Beach** (`/beach`) - Beach services and booking
- **Account** (`/account`) - User dashboard (auth required)
- **Booking** (`/booking`) - Booking management (auth required)

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_AI_SERVICE_URL=http://localhost:8001
```

### Tailwind Colors

Custom color palette defined in `style.css`:
- `ocean-deep` (50-900) - Primary blue
- `teal-glow` (50-900) - Secondary teal

## 📝 Development Notes

- All pages use shared `Navbar` and `Footer` components
- API calls centralized in `/api` directory
- Authentication handled via Pinia store
- Responsive breakpoints: xs(475px), sm(640px), md(768px), lg(1024px), xl(1280px)

## 🧹 Recent Cleanup

- Removed 15 duplicate/unused files
- Added shared Navbar and Footer components
- Improved code organization and consistency
- Reduced code duplication by ~40%

See [CLEANUP.md](./CLEANUP.md) for details.

## 📚 Documentation

- [STRUCTURE.md](./STRUCTURE.md) - Detailed project structure
- [CLEANUP.md](./CLEANUP.md) - Cleanup and refactoring notes
- [../LAYOUT_FIXES.md](../LAYOUT_FIXES.md) - Layout and styling fixes

## 🤝 Contributing

1. Follow Vue 3 Composition API best practices
2. Use TypeScript for type safety
3. Follow existing naming conventions
4. Keep components small and focused
5. Write responsive, mobile-first CSS

## 📄 License

Private - الخيمة Beach Resort
