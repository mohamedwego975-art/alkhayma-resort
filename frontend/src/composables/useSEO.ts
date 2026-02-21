/**
 * Composable for managing page meta tags
 */
export function useMeta(meta: {
  title?: string;
  description?: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  keywords?: string;
  robots?: string;
}) {
  const updateMeta = (key: string, value: string) => {
    let element = document.querySelector(`meta[name="${key}"]`);
    if (!element) {
      element = document.createElement("meta");
      element.setAttribute("name", key);
      document.head.appendChild(element);
    }
    element.setAttribute("content", value);
  };

  const updateOpenGraphMeta = (property: string, content: string) => {
    let element = document.querySelector(`meta[property="${property}"]`);
    if (!element) {
      element = document.createElement("meta");
      element.setAttribute("property", property);
      document.head.appendChild(element);
    }
    element.setAttribute("content", content);
  };

  if (meta.title) {
    document.title = meta.title;
    updateOpenGraphMeta("og:title", meta.title);
  }

  if (meta.description) {
    updateMeta("description", meta.description);
    updateOpenGraphMeta("og:description", meta.description);
  }

  if (meta.ogTitle) {
    updateOpenGraphMeta("og:title", meta.ogTitle);
  }

  if (meta.ogDescription) {
    updateOpenGraphMeta("og:description", meta.ogDescription);
  }

  if (meta.ogImage) {
    updateOpenGraphMeta("og:image", meta.ogImage);
  }

  if (meta.keywords) {
    updateMeta("keywords", meta.keywords);
  }

  if (meta.robots) {
    updateMeta("robots", meta.robots);
  }
}

/**
 * Composable for canonical URLs
 */
export function useCanonical(url: string) {
  let element = document.querySelector('link[rel="canonical"]');
  if (!element) {
    element = document.createElement("link");
    element.setAttribute("rel", "canonical");
    document.head.appendChild(element);
  }
  element.setAttribute("href", url);
}

/**
 * Composable for structured data (JSON-LD)
 */
export function useStructuredData(data: Record<string, any>) {
  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(data);
  document.head.appendChild(script);

  return () => {
    document.head.removeChild(script);
  };
}
