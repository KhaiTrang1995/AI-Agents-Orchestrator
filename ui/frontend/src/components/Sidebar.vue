<template>
  <aside
    class="w-full lg:w-80 lg:min-w-80 bg-white shadow-sm p-4 sm:p-6 overflow-y-auto border-b lg:border-b-0 lg:border-r border-gray-200"
  >
    <div class="space-y-6">
      <!-- Task Input -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <label class="block text-sm font-medium text-gray-700">
            Task Description
          </label>
          <div v-if="store.canFollowUp" class="flex items-center space-x-2">
            <label class="flex items-center space-x-1 cursor-pointer">
              <input
                v-model="conversationMode"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span class="text-xs text-gray-600">Conversation mode</span>
            </label>
          </div>
        </div>
        <textarea
          v-model="store.task"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          :placeholder="conversationMode && store.canFollowUp ? 'Continue with...' : 'Describe what you want to build...'"
          :disabled="store.isRunning"
          @keydown.enter.ctrl="handleExecute"
        ></textarea>
        <p v-if="conversationMode && store.canFollowUp" class="mt-1 text-xs text-green-600">
          💬 Messages will continue from previous task
        </p>
      </div>

      <!-- Workflow Selection -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Workflow
        </label>
        <select
          v-model="store.workflow"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="store.isRunning"
        >
          <option
            v-for="wf in workflowOptions"
            :key="wf.name"
            :value="wf.name"
          >
            {{ wf.label }}
          </option>
        </select>
      </div>

      <!-- Max Iterations -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Max Iterations
        </label>
        <input
          type="number"
          v-model.number="store.maxIterations"
          min="1"
          max="10"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="store.isRunning"
        />
      </div>

      <!-- Execute Button -->
      <button
        @click="handleExecute"
        :disabled="store.isRunning || !store.task.trim()"
        class="w-full px-4 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
      >
        {{ store.isRunning ? 'Executing...' : (conversationMode && store.canFollowUp ? 'Send Message' : 'Execute Task') }}
      </button>
      <p v-if="!conversationMode" class="mt-2 text-xs text-gray-500 text-center">
        Ctrl+Enter to execute
      </p>

      <!-- Follow-up Section -->
      <div v-if="store.canFollowUp && !store.isRunning" class="pt-6 border-t border-gray-200">
        <div class="flex items-center justify-between mb-2">
          <label class="block text-sm font-medium text-gray-700">
            Follow-up
          </label>
          <span class="text-xs text-green-600">✓ Ready</span>
        </div>
        <p class="text-xs text-gray-500 mb-2">
          Continue working on: "{{ store.lastTask.slice(0, 50) }}..."
        </p>
        <div class="flex flex-col sm:flex-row gap-2">
          <input
            v-model="followUpInput"
            type="text"
            placeholder="Add error handling..."
            class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            @keyup.enter="handleFollowUp"
          />
          <button
            @click="handleFollowUp"
            :disabled="!followUpInput.trim()"
            class="px-4 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            Go
          </button>
        </div>
      </div>

      <!-- Agents Status -->
      <div class="pt-6 border-t border-gray-200">
        <h3 class="text-sm font-medium text-gray-700 mb-3">Agents Status</h3>
        <div class="space-y-2">
          <div
            v-for="agent in store.agents"
            :key="agent.name"
            class="flex items-center justify-between text-sm"
          >
            <span class="text-gray-700 capitalize">{{ agent.name }}</span>
            <span :class="agent.available ? 'text-green-600' : 'text-gray-400'">
              {{ agent.available ? '✓' : '○' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Local Models Status -->
      <div class="pt-6 border-t border-gray-200">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-medium text-gray-700">Local Models</h3>
          <button
            @click="store.loadLocalModelStatus()"
            class="text-xs px-2 py-1 rounded border border-gray-300 text-gray-600 hover:bg-gray-50"
            :disabled="store.isRunning"
          >
            Refresh
          </button>
        </div>

        <div v-if="store.hasLocalModelStatus" class="space-y-3">
          <div
            v-for="backend in localBackends"
            :key="`${backend.backend_type}-${backend.endpoint}`"
            class="rounded-md border border-gray-200 p-2"
          >
            <div class="flex items-center justify-between text-xs">
              <span class="font-semibold text-gray-700">{{ backend.backend_type }}</span>
              <span :class="backend.online ? 'text-green-600' : 'text-red-600'">
                {{ backend.online ? '● Online' : '○ Offline' }}
              </span>
            </div>
            <div class="text-xs text-gray-500 break-all mt-1">{{ backend.endpoint }}</div>
            <div class="text-xs text-gray-600 mt-1">
              Agents: {{ backend.agents.join(', ') }}
            </div>
            <div class="text-xs text-gray-600">
              Models: {{ backend.model_count }}
            </div>
            <div v-if="backend.models_detailed?.length" class="mt-2 flex flex-wrap gap-1">
              <span
                v-for="model in backend.models_detailed.slice(0, 6)"
                :key="model.name || model.id"
                class="text-[10px] px-2 py-0.5 rounded-full bg-gray-100 text-gray-700"
              >
                {{ formatModelLabel(model) }}
              </span>
            </div>
            <div
              v-else-if="backend.models?.length"
              class="mt-2 text-[10px] text-gray-600 break-words"
            >
              {{ backend.models.slice(0, 6).join(', ') }}
            </div>
            <div v-if="backend.probe_error" class="mt-1 text-[10px] text-amber-700">
              {{ backend.probe_error }}
            </div>
          </div>

          <div class="space-y-1">
            <div
              v-for="agent in localAgents"
              :key="agent.name"
              class="text-xs flex items-center justify-between gap-2"
            >
              <span class="text-gray-700 truncate">{{ agent.name }}</span>
              <span :class="agent.available_for_execution ? 'text-green-600' : 'text-gray-500'">
                {{ agent.available_for_execution ? 'ready' : 'not-ready' }}
              </span>
            </div>
          </div>
        </div>
        <p v-else class="text-xs text-gray-500">
          No local model backends configured.
        </p>
      </div>

      <!-- Live Progress Logs -->
      <div v-if="store.isRunning" class="pt-6 border-t border-gray-200">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-sm font-medium text-gray-700">Live Progress</h3>
          <span class="text-xs text-blue-600 animate-pulse">● Running</span>
        </div>
        <div
          v-if="store.hasLogs"
          class="bg-gray-900 rounded-lg p-3 max-h-40 overflow-y-auto font-mono text-xs"
        >
          <div
            v-for="log in store.logs.slice(-5)"
            :key="log.id"
            :class="{
              'text-blue-400': log.level === 'info',
              'text-green-400': log.level === 'success',
              'text-yellow-400': log.level === 'warn' || log.level === 'warning',
              'text-red-400': log.level === 'error',
              'text-gray-400': !['info', 'success', 'warn', 'warning', 'error'].includes(log.level)
            }"
            class="mb-1"
          >
            {{ log.message }}
          </div>
        </div>
        <p v-if="store.hasLogs" class="mt-1 text-xs text-gray-500 text-center">
          View all logs in the Logs tab
        </p>
        <p v-else class="mt-1 text-xs text-gray-500 text-center">
          Waiting for execution logs...
        </p>
      </div>

      <!-- Files Created -->
      <div v-if="store.hasFiles" class="pt-6 border-t border-gray-200">
        <h3 class="text-sm font-medium text-gray-700 mb-3">Generated Files</h3>
        <div class="space-y-1">
          <button
            v-for="file in store.files"
            :key="file"
            @click="store.loadFile(file)"
            class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition"
          >
            📄 {{ file }}
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useOrchestratorStore } from '../stores/orchestrator'

const store = useOrchestratorStore()
const followUpInput = ref('')
const conversationMode = ref(false)
const localBackends = computed(() => store.localModelStatus?.backends || [])
const localAgents = computed(() => store.localModelStatus?.agents || [])

const workflowOptions = computed(() => {
  if (store.workflows.length > 0) {
    return store.workflows.map((wf) => ({
      name: wf.name,
      label: wf.description ? `${wf.name} (${wf.description})` : wf.name
    }))
  }

  return [
    { name: 'default', label: 'default (Codex → Gemini → Claude)' },
    { name: 'quick', label: 'quick (Codex only)' },
    { name: 'thorough', label: 'thorough (multi-review)' },
    { name: 'review-only', label: 'review-only' },
    { name: 'document', label: 'document' }
  ]
})

const formatBytes = (bytes) => {
  if (!Number.isFinite(bytes) || bytes <= 0) return ''
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let size = bytes
  let unitIdx = 0
  while (size >= 1024 && unitIdx < units.length - 1) {
    size /= 1024
    unitIdx += 1
  }
  return `${size.toFixed(size >= 100 || unitIdx === 0 ? 0 : 1)}${units[unitIdx]}`
}

const formatModelLabel = (model) => {
  if (!model || typeof model !== 'object') return String(model || '')
  const name = model.name || model.id || 'unknown-model'
  const size = model.size_bytes ? ` (${formatBytes(Number(model.size_bytes))})` : ''
  return `${name}${size}`
}

// Auto-enable conversation mode when follow-up becomes available
watch(() => store.canFollowUp, (canFollowUp) => {
  if (canFollowUp && !conversationMode.value) {
    // Don't auto-enable, let user choose
  }
})

const handleExecute = () => {
  if (conversationMode.value && store.canFollowUp) {
    // Execute as follow-up
    store.executeFollowUp(store.task)
  } else {
    // Execute as new task
    store.executeTask()
    conversationMode.value = false // Reset conversation mode
  }
}

const handleFollowUp = () => {
  if (followUpInput.value.trim()) {
    store.executeFollowUp(followUpInput.value)
    followUpInput.value = ''
  }
}
</script>
