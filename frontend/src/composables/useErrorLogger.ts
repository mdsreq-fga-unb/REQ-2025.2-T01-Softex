import { ref } from 'vue'

export interface ErrorLog {
  id: string
  timestamp: Date
  type: 'error' | 'warning' | 'info'
  message: string
  details?: any
  context?: string
  stack?: string
}

const errorLogs = ref<ErrorLog[]>([])
const maxLogs = 100 // Limite de logs mantidos em memória

/**
 * Composable para gerenciar logs de erros
 */
export function useErrorLogger() {
  /**
   * Adiciona um log de erro
   */
  const logError = (
    message: string,
    details?: any,
    context?: string,
    error?: Error
  ) => {
    const log: ErrorLog = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      type: 'error',
      message,
      details,
      context,
      stack: error?.stack
    }

    errorLogs.value.unshift(log)
    
    // Limita o número de logs
    if (errorLogs.value.length > maxLogs) {
      errorLogs.value = errorLogs.value.slice(0, maxLogs)
    }

    // Log no console
    console.error(`[ERROR] ${context ? `[${context}]` : ''} ${message}`, details || '', error || '')

    // Aqui você pode adicionar integração com serviços externos de logging
    // como Sentry, LogRocket, etc.
  }

  /**
   * Adiciona um log de warning
   */
  const logWarning = (
    message: string,
    details?: any,
    context?: string
  ) => {
    const log: ErrorLog = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      type: 'warning',
      message,
      details,
      context
    }

    errorLogs.value.unshift(log)
    
    if (errorLogs.value.length > maxLogs) {
      errorLogs.value = errorLogs.value.slice(0, maxLogs)
    }

    console.warn(`[WARNING] ${context ? `[${context}]` : ''} ${message}`, details || '')
  }

  /**
   * Adiciona um log de informação
   */
  const logInfo = (
    message: string,
    details?: any,
    context?: string
  ) => {
    const log: ErrorLog = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      type: 'info',
      message,
      details,
      context
    }

    errorLogs.value.unshift(log)
    
    if (errorLogs.value.length > maxLogs) {
      errorLogs.value = errorLogs.value.slice(0, maxLogs)
    }

    console.info(`[INFO] ${context ? `[${context}]` : ''} ${message}`, details || '')
  }

  /**
   * Limpa todos os logs
   */
  const clearLogs = () => {
    errorLogs.value = []
  }

  /**
   * Obtém todos os logs
   */
  const getLogs = () => {
    return errorLogs.value
  }

  /**
   * Obtém logs filtrados por tipo
   */
  const getLogsByType = (type: ErrorLog['type']) => {
    return errorLogs.value.filter(log => log.type === type)
  }

  /**
   * Exporta logs para JSON
   */
  const exportLogs = () => {
    return JSON.stringify(errorLogs.value, null, 2)
  }

  return {
    errorLogs,
    logError,
    logWarning,
    logInfo,
    clearLogs,
    getLogs,
    getLogsByType,
    exportLogs
  }
}

