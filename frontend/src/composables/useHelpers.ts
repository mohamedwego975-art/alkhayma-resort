import { ref, watch } from "vue";

/**
 * Composable for syncing state with localStorage
 */
export function useLocalStorage<T>(key: string, initialValue: T) {
  // Get from local storage or use initial value
  const read = (): T => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  };

  const data = ref<T>(read());

  // Watch changes and update localStorage
  watch(
    data,
    (newValue) => {
      try {
        localStorage.setItem(key, JSON.stringify(newValue));
      } catch {
        console.warn(`Failed to save to localStorage: ${key}`);
      }
    },
    { deep: true },
  );

  return data;
}

/**
 * Composable for async operations
 */
export function useAsync<T>(asyncFn: () => Promise<T>) {
  const data = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const execute = async () => {
    loading.value = true;
    error.value = null;
    try {
      data.value = await asyncFn();
    } catch (err) {
      error.value = err instanceof Error ? err : new Error("Unknown error");
    } finally {
      loading.value = false;
    }
  };

  return {
    data,
    loading,
    error,
    execute,
  };
}

/**
 * Composable for form validation
 */
export function useForm<T extends Record<string, any>>(initialValues: T) {
  const values = ref<T>({ ...initialValues });
  const errors = ref<Record<string, string>>({});
  const touched = ref<Record<string, boolean>>({});

  const setFieldValue = (field: keyof T, value: any) => {
    values.value[field] = value;
  };

  const setFieldError = (field: string, error: string) => {
    errors.value[field] = error;
  };

  const setFieldTouched = (field: string) => {
    touched.value[field] = true;
  };

  const resetForm = () => {
    values.value = { ...initialValues };
    errors.value = {};
    touched.value = {};
  };

  return {
    values,
    errors,
    touched,
    setFieldValue,
    setFieldError,
    setFieldTouched,
    resetForm,
  };
}

/**
 * Composable for debouncing
 */
export function useDebounce<T>(value: T, delay: number = 500) {
  const debounced = ref(value);
  let timeout: ReturnType<typeof setTimeout>;

  watch(
    () => value,
    (newValue) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        debounced.value = newValue;
      }, delay);
    },
  );

  return debounced;
}

/**
 * Composable for throttling
 */
export function useThrottle<T>(value: T, interval: number = 500) {
  const throttled = ref(value);
  let lastUpdate = 0;

  const update = () => {
    const now = Date.now();
    if (now - lastUpdate >= interval) {
      throttled.value = value;
      lastUpdate = now;
    }
  };

  watch(() => value, update);

  return throttled;
}

/**
 * Composable for intersection observer
 */
export function useIntersectionObserver(callback: (isVisible: boolean) => void, options = {}) {
  const element = ref<HTMLElement | null>(null);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      callback(entry.isIntersecting);
    });
  }, options);

  const observe = (el: HTMLElement) => {
    element.value = el;
    observer.observe(el);
  };

  const unobserve = () => {
    if (element.value) {
      observer.unobserve(element.value);
    }
  };

  return { observe, unobserve };
}
