import { ref, computed } from 'vue'
import type { Ref } from 'vue'

export interface Product {
  id: string
  name: string
  type: 'room' | 'activity' | 'package'
  price: number
  capacity: number
  tags: string[]
}

export interface Suggestion {
  product: Product
  reason: string
  confidence: number
  savings?: number
}

export function useSmartSuggest(
  currentProduct: Ref<Product | null>,
  allProducts: Ref<Product[]>
) {
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const suggestions = computed<Suggestion[]>(() => {
    if (!currentProduct.value || allProducts.value.length === 0) {
      return []
    }

    const current = currentProduct.value
    const suggestions: Suggestion[] = []

    // Rule 1: Suggest upgrades (higher capacity, similar type)
    const upgrades = allProducts.value.filter(p => 
      p.type === current.type &&
      p.capacity > current.capacity &&
      p.id !== current.id
    )

    upgrades.forEach(product => {
      suggestions.push({
        product,
        reason: `More space for your group (+${product.capacity - current.capacity} people)`,
        confidence: 0.8,
        savings: Math.max(0, current.price - product.price)
      })
    })

    // Rule 2: Suggest complementary products
    const complementary = allProducts.value.filter(p =>
      p.type !== current.type &&
      !suggestions.some(s => s.product.id === p.id)
    )

    complementary.forEach(product => {
      let reason = ''
      let confidence = 0.6

      if (product.type === 'activity' && current.type === 'room') {
        reason = 'Perfect activity to enjoy during your stay'
        confidence = 0.75
      } else if (product.type === 'package' && current.type === 'room') {
        reason = 'Bundle and save with this exclusive package'
        confidence = 0.85
      } else {
        reason = 'Guests often book this together'
        confidence = 0.6
      }

      suggestions.push({
        product,
        reason,
        confidence,
        savings: product.type === 'package' ? Math.floor(product.price * 0.15) : undefined
      })
    })

    // Rule 3: Similar items (same tags)
    const similarTags = allProducts.value.filter(p =>
      p.id !== current.id &&
      p.tags.some(tag => current.tags.includes(tag)) &&
      !suggestions.some(s => s.product.id === p.id)
    )

    similarTags.forEach(product => {
      const commonTags = product.tags.filter(tag => current.tags.includes(tag))
      suggestions.push({
        product,
        reason: `Similar to your choice (${commonTags.join(', ')})`,
        confidence: 0.7
      })
    })

    // Sort by confidence descending
    return suggestions
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 5)
  })

  const bestSuggestion = computed(() => {
    return suggestions.value[0] || null
  })

  const fetchAIRecommendations = async (userPreferences?: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('http://localhost:8001/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_product_id: currentProduct.value?.id,
          user_preferences: userPreferences,
          all_products: allProducts.value
        })
      })

      if (!response.ok) throw new Error('Failed to fetch recommendations')

      const data = await response.json()
      return data.recommendations as Suggestion[]
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error'
      return []
    } finally {
      isLoading.value = false
    }
  }

  const getSuggestionFor = (productType: string): Suggestion | null => {
    return suggestions.value.find(s => s.product.type === productType) || null
  }

  return {
    suggestions,
    bestSuggestion,
    isLoading,
    error,
    fetchAIRecommendations,
    getSuggestionFor
  }
}
