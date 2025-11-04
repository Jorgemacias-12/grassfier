import {
  ChartColumn,
  Clock,
  Leaf,
  Shield,
  Smartphone,
  Zap,
} from "@lucide/astro";

export const navigationItems = [
  {
    title: "Clasificador",
    href: "#clasfier",
  },
  { title: "Características", href: "#features" },
  { title: "Acerca de", href: "#about" },
];

export type NavigationItems = typeof navigationItems;

export const heroFacts = [
  {
    title: "98%",
    subtitle: "Precisión",
  },
  {
    title: "50+",
    subtitle: "Enfermedades",
  },
  {
    title: "Instantaneos",
    subtitle: "Resultados",
  },
];

export type HeroFacts = typeof heroFacts;

export const footerLinks = [
  {
    title: "Producto",
    subLinks: [
      {
        label: "Caracteristicas",
        href: "#",
      },
      {
        label: "Precios",
        href: "#",
      },
      {
        label: "Documentación",
        href: "#",
      },
    ],
  },
  {
    title: "Empresa",
    subLinks: [
      {
        label: "Acerca de",
        href: "#",
      },
      {
        label: "Blog",
        href: "#",
      },
      {
        label: "Contact",
        href: "#",
      },
    ],
  },
  {
    title: "Legal",
    subLinks: [
      {
        label: "Privicidad",
        href: "#",
      },
      {
        label: "Términos",
        href: "#",
      },
      {
        label: "Cookies",
        href: "#",
      },
    ],
  },
];

export type FooterLinks = typeof footerLinks;

export const footerSocialLinks = [
  {
    title: "X",
    href: "#X",
  },
  {
    title: "LinkedIn",
    href: "#LinkedIn",
  },
  {
    title: "GitHub",
    href: "#GitHub",
  },
];

export type FooterSocialLinks = typeof footerSocialLinks;

export const featureList = [
  {
    icon: Leaf,
    title: "Detección Precisa",
    caption:
      "Identifica más de 50 enfermedades comunes en plantas con 98% de precisión",
  },
  {
    icon: Zap,
    title: "Análisis Instantáneo",
    caption: "Obtén resultados en segundos, no en horas o días",
  },
  {
    icon: ChartColumn,
    title: "Reportes Detallados",
    caption:
      "Análisis completo con recomendaciones de tratamiento personalizadas",
  },
  {
    icon: Shield,
    title: "Protección de Cultivos",
    caption:
      "Intervención temprana para maximizar rendimiento y minimizar pérdidas",
  },
  {
    icon: Clock,
    title: "Monitoreo Continuo",
    caption:
      "Realiza seguimiento del progreso de tus plantas a lo largo del tiempo",
  },
  {
    icon: Smartphone,
    title: "Acceso Móvil",
    caption:
      "Analiza tus plantas desde cualquier lugar con tu dispositivo móvil",
  },
];

export type FeatureList = typeof featureList;
