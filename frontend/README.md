# Sentinel no Yaiba - Frontend

Frontend React avec TypeScript, GlassUI (glassmorphism), et i18n pour le dashboard de sécurité Sentinel no Yaiba.

## 🚀 Technologies

- **React 18** avec TypeScript
- **Vite** pour le build
- **Tailwind CSS** pour le styling avec glassmorphism
- **react-i18next** pour l'internationalisation (FR/EN)
- **Zustand** pour la gestion d'état
- **React Router** pour la navigation
- **Recharts** pour les graphiques
- **Lucide React** pour les icônes
- **Axios** pour les appels API

## 📦 Installation

```bash
cd frontend
npm install
```

## 🏃 Développement

```bash
npm run dev
```

L'application sera disponible sur http://localhost:5173

## 🏗️ Structure

```
frontend/
├── src/
│   ├── components/        # Composants réutilisables
│   │   ├── auth/         # Composants d'authentification
│   │   ├── common/       # Composants communs
│   │   ├── dashboard/    # Composants du dashboard
│   │   ├── layout/       # Composants de layout
│   │   ├── threats/      # Composants de menaces
│   │   └── admin/        # Composants admin
│   ├── pages/            # Pages de l'application
│   ├── services/         # Services API et mock data
│   ├── store/            # Stores Zustand
│   ├── types/            # Types TypeScript
│   ├── i18n/             # Configuration i18n
│   └── App.tsx           # Composant principal
```

## 🎨 GlassUI (Glassmorphism)

Le design utilise le glassmorphism avec les classes utilitaires:
- `.glass` - Effet de verre léger
- `.glass-strong` - Effet de verre plus prononcé
- `.glass-hover` - Effet hover sur les éléments glass

## 🌍 Internationalisation

L'application supporte le français (par défaut) et l'anglais. Les traductions sont dans:
- `src/i18n/locales/fr.json`
- `src/i18n/locales/en.json`

Le changement de langue se fait via le composant `LanguageSwitcher` dans le header.

## 🔐 Authentification

L'authentification utilise:
- JWT tokens (access + refresh)
- Stockage dans localStorage
- Fallback sur mock data si l'API n'est pas disponible

**Comptes de démonstration:**
- Username: `admin` / Password: `password` (rôle admin)
- Username: `client1` / Password: `password` (rôle client)

## 📊 Mock Data

Le frontend fonctionne avec des données mockées si l'API backend n'est pas disponible. Les données mockées sont dans `src/services/mockData.ts`.

## 🧪 Build

```bash
npm run build
```

Le build sera dans le dossier `dist/`.

## 📝 Notes

- Le frontend est configuré pour se connecter au backend sur `http://localhost:8000`
- Les routes API sont proxifiées via Vite
- Le WebSocket est configuré pour `ws://localhost:8000/ws`

