<template>
  <div class="p-4 sm:p-6">
    <!-- Tabs -->
    <div class="mb-4">
      <nav class="flex space-x-2 sm:space-x-4 border-b border-gray-200 overflow-x-auto">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-3 sm:px-4 py-2 text-sm font-medium border-b-2 transition whitespace-nowrap',
            activeTab === tab.id
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Tab Content -->
    <div class="space-y-4">
      <!-- Output Tab -->
      <div v-show="activeTab === 'output'" class="bg-white rounded-lg shadow-sm p-4 sm:p-6">
        <div v-if="store.isRunning" class="mb-4 border border-blue-100 bg-blue-50 rounded-lg p-4">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-semibold text-blue-800">Execution In Progress</h3>
            <span class="text-xs text-blue-700 animate-pulse">● Running</span>
          </div>
          <p class="text-sm text-blue-900 mb-3">
            The task is currently executing. Live events will appear below.
          </p>
          <div
            v-if="store.hasLogs"
            class="bg-slate-900 rounded-md p-3 max-h-44 overflow-y-auto font-mono text-xs"
          >
            <div
              v-for="log in store.logs.slice(-8)"
              :key="log.id"
              :class="{
                'text-blue-300': log.level === 'info',
                'text-green-300': log.level === 'success',
                'text-yellow-300': log.level === 'warn' || log.level === 'warning',
                'text-red-300': log.level === 'error',
                'text-gray-300': !['info', 'success', 'warn', 'warning', 'error'].includes(log.level)
              }"
              class="mb-1"
            >
              [{{ log.time }}] {{ log.message }}
            </div>
          </div>
          <div v-else class="text-xs text-blue-700 italic">
            Waiting for progress events...
          </div>
        </div>

        <div v-if="store.hasOutput" class="prose max-w-none">
          <pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">{{ store.output }}</pre>
        </div>
        <div v-else class="text-gray-500 italic text-center py-12">
          {{ store.isRunning ? 'Execution is running. Output will appear here when available...' : 'Output will appear here after task execution...' }}
        </div>
      </div>

      <!-- Editor Tab -->
      <div v-show="activeTab === 'editor'" class="bg-white rounded-lg shadow-sm p-4">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <span class="text-sm font-medium text-gray-700">
              {{ store.currentFile?.filename || 'No file selected' }}
            </span>
          </div>
          <div v-if="store.currentFile" class="flex space-x-2">
            <button
              @click="downloadFile"
              class="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
            >
              Download
            </button>
          </div>
        </div>
        <MonacoEditor />
      </div>

      <!-- Iterations Tab -->
      <div v-show="activeTab === 'iterations'">
        <div v-if="store.iterations.length > 0" class="space-y-4">
          <div
            v-for="(iteration, i) in store.iterations"
            :key="i"
            class="bg-white rounded-lg shadow-sm p-4"
          >
            <h4 class="font-medium text-gray-900 mb-3">Iteration {{ i + 1 }}</h4>
            <div class="space-y-2">
              <div
                v-for="(step, j) in iteration.steps"
                :key="j"
                class="flex items-start space-x-2"
              >
                <span :class="step.success ? 'text-green-600' : 'text-red-600'">
                  {{ step.success ? '✓' : '✗' }}
                </span>
                <div class="flex-1">
                  <div class="text-sm font-medium">
                    {{ step.agent }} - {{ step.task }}
                  </div>
                  <div v-if="step.suggestions" class="text-xs text-gray-500">
                    {{ step.suggestions.length }} suggestions
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="bg-white rounded-lg shadow-sm p-6 text-gray-500 italic text-center">
          Iteration details will appear here...
        </div>
      </div>

      <!-- Logs Tab -->
      <div v-show="activeTab === 'logs'" class="bg-white rounded-lg shadow-sm p-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Execution Logs</h3>
          <button
            v-if="store.hasLogs"
            @click="store.clearLogs()"
            class="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 transition"
          >
            Clear Logs
          </button>
        </div>
        <div v-if="store.hasLogs" class="bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto font-mono text-sm">
          <div
            v-for="log in store.logs"
            :key="log.id"
            class="flex items-start space-x-2 mb-1"
          >
            <span class="text-gray-500 text-xs flex-shrink-0">{{ log.time }}</span>
            <span
              :class="{
                'text-blue-400': log.level === 'info',
                'text-green-400': log.level === 'success',
                'text-yellow-400': log.level === 'warn' || log.level === 'warning',
                'text-red-400': log.level === 'error',
                'text-gray-400': !['info', 'success', 'warn', 'warning', 'error'].includes(log.level)
              }"
              class="flex-1"
            >
              <span class="font-semibold">[{{ log.level.toUpperCase() }}]</span> {{ log.message }}
            </span>
          </div>
        </div>
        <div v-else class="text-gray-500 italic text-center py-12">
          Execution logs will appear here in real-time...
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useOrchestratorStore } from '../stores/orchestrator'
import MonacoEditor from './MonacoEditor.vue'

const store = useOrchestratorStore()

const activeTab = ref('output')
const tabs = [
  { id: 'output', label: 'Output' },
  { id: 'editor', label: 'Code Editor' },
  { id: 'iterations', label: 'Iterations' },
  { id: 'logs', label: 'Logs' }
]

const downloadFile = () => {
  if (store.currentFile) {
    store.downloadFile(store.currentFile.filename, store.fileContent)
  }
}
</script>
