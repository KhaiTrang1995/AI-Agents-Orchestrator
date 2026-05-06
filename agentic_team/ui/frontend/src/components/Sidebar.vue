<template>
  <aside
    class="w-full lg:w-80 lg:min-w-80 bg-slate-900 border-b lg:border-b-0 lg:border-r border-cyan-500/20 overflow-y-auto flex-shrink-0"
  >
    <div class="p-4 space-y-5">

      <!-- Task Input -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <label class="block text-xs font-semibold text-cyan-300/80 uppercase tracking-wider">
            Task for Team
          </label>
          <div v-if="store.canFollowUp" class="flex items-center space-x-2">
            <label class="flex items-center space-x-1.5 cursor-pointer group">
              <div class="relative">
                <input
                  v-model="conversationMode"
                  type="checkbox"
                  class="sr-only peer"
                />
                <div class="w-8 h-4 bg-slate-700 peer-checked:bg-cyan-600 rounded-full transition-colors duration-200 cursor-pointer"></div>
                <div class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow transition-transform duration-200 peer-checked:translate-x-4"></div>
              </div>
              <span class="text-xs text-slate-400 group-hover:text-cyan-300 transition-colors">Chat mode</span>
            </label>
          </div>
        </div>
        <textarea
          v-model="store.task"
          rows="4"
          class="w-full px-3 py-2.5 bg-slate-800 border border-cyan-500/20 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/60 resize-y transition-all duration-150 font-mono min-h-[6rem] max-h-80"
          :placeholder="conversationMode && store.canFollowUp ? 'Continue the conversation...' : 'Describe what you want to build...'"
          :disabled="store.isRunning"
          @keydown.enter.ctrl="handleExecute"
        ></textarea>
        <!-- File upload to inject context -->
        <div class="mt-2 flex items-center gap-2">
          <input
            ref="fileInputRef"
            type="file"
            accept=".txt,.md,.pdf"
            class="hidden"
            @change="handleFileUpload"
          />
          <button
            @click="fileInputRef.click()"
            :disabled="store.isRunning"
            class="flex items-center gap-1.5 px-2.5 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 border border-cyan-500/20 hover:border-cyan-500/40 text-slate-400 hover:text-cyan-300 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            title="Attach .txt, .md, or .pdf file to inject as context"
          >
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
            Attach file
          </button>
          <span v-if="attachedFileName" class="text-[10px] text-cyan-400/80 font-mono truncate flex-1">
            {{ attachedFileName }}
          </span>
          <button
            v-if="attachedFileName"
            @click="clearAttachment"
            class="text-slate-600 hover:text-red-400 transition-colors flex-shrink-0"
            title="Remove attachment"
          >✕</button>
        </div>
        <p v-if="conversationMode && store.canFollowUp" class="mt-1.5 text-xs text-teal-400/80 flex items-center gap-1">
          <span class="w-1.5 h-1.5 rounded-full bg-teal-400 inline-block"></span>
          Messages continue from previous task
        </p>
      </div>

      <!-- Workflow Selection -->
      <div>
        <label class="block text-xs font-semibold text-cyan-300/80 uppercase tracking-wider mb-2">
          Workflow
        </label>
        <select
          v-model="store.workflow"
          class="w-full px-3 py-2 bg-slate-800 border border-cyan-500/20 rounded-xl text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/60 transition-all cursor-pointer"
          :disabled="store.isRunning"
        >
          <option
            v-for="wf in workflowOptions"
            :key="wf.name"
            :value="wf.name"
            class="bg-slate-800"
          >
            {{ wf.label }}
          </option>
        </select>
      </div>

      <!-- Max Iterations -->
      <div>
        <label class="block text-xs font-semibold text-cyan-300/80 uppercase tracking-wider mb-2">
          Max Iterations
        </label>
        <input
          type="number"
          v-model.number="store.maxIterations"
          min="1"
          max="10"
          class="w-full px-3 py-2 bg-slate-800 border border-cyan-500/20 rounded-xl text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/60 transition-all"
          :disabled="store.isRunning"
        />
      </div>

      <!-- HITL Toggle -->
      <div class="flex items-center justify-between py-2.5 px-3 rounded-xl bg-slate-800/60 border border-slate-700/60">
        <div class="flex items-center gap-2">
          <svg class="w-3.5 h-3.5 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="text-xs text-slate-300">Human-in-the-Loop</span>
        </div>
        <label class="flex items-center gap-1.5 cursor-pointer">
          <span class="text-[10px]" :class="store.hitlEnabled ? 'text-amber-400' : 'text-slate-600'">{{ store.hitlEnabled ? 'ON' : 'OFF' }}</span>
          <div class="relative">
            <input v-model="store.hitlEnabled" type="checkbox" class="sr-only peer" :disabled="store.isRunning || store.isPaused" />
            <div class="w-8 h-4 bg-slate-700 peer-checked:bg-amber-500/70 rounded-full transition-colors cursor-pointer"></div>
            <div class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow transition-transform peer-checked:translate-x-4"></div>
          </div>
        </label>
      </div>

      <!-- Execute / Cancel / Pause Buttons -->
      <div class="space-y-2">
        <button
          v-if="!store.isRunning && !store.isPaused"
          @click="handleExecute"
          :disabled="!store.task.trim()"
          class="w-full px-4 py-2.5 bg-gradient-to-r from-teal-500 via-cyan-500 to-blue-500 hover:from-teal-400 hover:via-cyan-400 hover:to-blue-400 text-white text-sm font-semibold rounded-xl shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none transition-all duration-150 active:scale-[0.98]"
        >
          {{ conversationMode && store.canFollowUp ? 'Send Message' : 'Start Team' }}
        </button>

        <!-- Running: Pause + Stop -->
        <template v-if="store.isRunning">
          <button
            @click="store.pauseExecution()"
            class="w-full px-4 py-2.5 bg-amber-600/20 hover:bg-amber-600/30 border border-amber-500/50 hover:border-amber-500/70 text-amber-400 hover:text-amber-300 text-sm font-semibold rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500/40 transition-all duration-150 active:scale-[0.98] flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
            Pause & Review
          </button>
          <button
            @click="handleCancel"
            class="w-full px-4 py-2.5 bg-rose-600/20 hover:bg-rose-600/30 border border-rose-500/50 hover:border-rose-500/70 text-rose-400 hover:text-rose-300 text-sm font-semibold rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-500/40 transition-all duration-150 active:scale-[0.98] flex items-center justify-center gap-2"
          >
            <span class="w-2 h-2 rounded-sm bg-rose-500 inline-block"></span>
            Stop Team
          </button>
        </template>

        <!-- Paused: HITL Approval Panel -->
        <div v-if="store.isPaused" class="rounded-xl border border-amber-500/40 bg-amber-500/5 p-3 space-y-3">
          <div class="flex items-center gap-2">
            <span class="relative flex h-2.5 w-2.5 flex-shrink-0">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
            </span>
            <span class="text-xs font-semibold text-amber-300">Awaiting Approval</span>
          </div>
          <div v-if="store.hitlPending" class="space-y-1">
            <p class="text-[11px] text-slate-400">
              <span class="text-slate-500">Agent:</span>
              <span class="ml-1 text-cyan-300 font-mono">{{ store.hitlPending.agent }}</span>
            </p>
            <p class="text-[11px] text-slate-400">
              <span class="text-slate-500">Step:</span>
              <span class="ml-1 text-amber-300 font-mono">{{ store.hitlPending.step }}</span>
            </p>
            <p v-if="store.hitlPending.description" class="text-[11px] text-slate-500 leading-relaxed mt-1">
              {{ store.hitlPending.description }}
            </p>
          </div>
          <div v-else class="text-[11px] text-slate-500 italic">Execution paused by user</div>
          <div class="flex gap-2 pt-1">
            <button
              @click="store.approveHitl()"
              class="flex-1 px-3 py-2 bg-emerald-600/20 hover:bg-emerald-600/30 border border-emerald-500/50 text-emerald-400 hover:text-emerald-300 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5"
            >
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
              Approve
            </button>
            <button
              @click="store.rejectHitl()"
              class="flex-1 px-3 py-2 bg-rose-600/20 hover:bg-rose-600/30 border border-rose-500/50 text-rose-400 hover:text-rose-300 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5"
            >
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
              Reject
            </button>
          </div>
        </div>

        <p v-if="!store.isRunning && !store.isPaused && !conversationMode" class="text-xs text-slate-500 text-center">
          Ctrl+Enter to start
        </p>
      </div>

      <!-- Follow-up Section -->
      <div v-if="store.canFollowUp && !store.isRunning" class="pt-4 border-t border-slate-700/60">
        <div class="flex items-center justify-between mb-2">
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Follow-up
          </label>
          <span class="text-xs text-emerald-400 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
            Ready
          </span>
        </div>
        <p class="text-xs text-slate-500 mb-2 truncate">
          Last: "{{ store.lastTask.slice(0, 45) }}..."
        </p>
        <div class="flex gap-2">
          <input
            v-model="followUpInput"
            type="text"
            placeholder="Add error handling..."
            class="flex-1 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/40 focus:border-emerald-500/40 transition-all"
            @keyup.enter="handleFollowUp"
          />
          <button
            @click="handleFollowUp"
            :disabled="!followUpInput.trim()"
            class="px-3 py-2 text-xs bg-emerald-600/20 hover:bg-emerald-600/30 border border-emerald-500/40 hover:border-emerald-500/60 text-emerald-400 hover:text-emerald-300 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            Go
          </button>
        </div>
      </div>

      <!-- Agents Status -->
      <div class="pt-4 border-t border-slate-700/60">
        <h3 class="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">Agents</h3>
        <div class="space-y-1.5">
          <div
            v-for="agent in store.agents"
            :key="agent.name"
            class="flex items-center justify-between py-1.5 px-2.5 rounded-md bg-slate-800/50 hover:bg-slate-800 transition-colors"
          >
            <span class="text-xs text-slate-300 capitalize font-mono">{{ agent.name }}</span>
            <div class="flex items-center gap-1.5">
              <!-- dynamic status when running -->
              <template v-if="store.isRunning && agentRunStatus(agent.name).label !== 'idle'">
                <svg class="w-3 h-3 animate-spin" :class="agentRunStatus(agent.name).spinColor" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
                </svg>
                <span :class="agentRunStatus(agent.name).textColor" class="text-xs">
                  {{ agentRunStatus(agent.name).label }}
                </span>
              </template>
              <!-- static status when idle -->
              <template v-else>
                <span
                  :class="agent.available ? 'bg-emerald-400 shadow-emerald-400/50' : 'bg-slate-600'"
                  class="w-1.5 h-1.5 rounded-full shadow-sm"
                ></span>
                <span :class="agent.available ? 'text-emerald-400' : 'text-slate-500'" class="text-xs">
                  {{ agent.available ? 'ready' : 'off' }}
                </span>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Local Models Status -->
      <div class="pt-4 border-t border-slate-700/60">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-xs font-semibold text-cyan-300/80 uppercase tracking-wider">Local Models</h3>
          <button
            @click="store.loadLocalModelStatus()"
            class="text-xs px-2 py-1 rounded-md border border-cyan-500/30 text-cyan-300/80 hover:text-cyan-200 hover:border-cyan-400/60 hover:bg-cyan-500/10 transition-all"
            :disabled="store.isRunning"
          >
            Refresh
          </button>
        </div>
        <p class="text-xs text-amber-300/90">
          Limitation: local adapters return text output only and do not directly edit files.
        </p>
        <p class="text-xs text-slate-500 mt-1.5 mb-2.5">
          Best use: offline drafting, role handoff input, review feedback, and fallback.
        </p>

        <div v-if="store.hasLocalModelStatus" class="space-y-2.5">
          <div
            v-for="backend in localBackends"
            :key="`${backend.backend_type}-${backend.endpoint}`"
            class="rounded-xl border border-cyan-500/20 bg-slate-800/60 p-2.5 space-y-1.5"
          >
            <div class="flex items-center justify-between text-xs">
              <span class="font-semibold text-slate-200 font-mono">{{ backend.backend_type }}</span>
              <span
                :class="backend.online ? 'text-emerald-400' : 'text-rose-400'"
                class="flex items-center gap-1"
              >
                <span :class="backend.online ? 'bg-emerald-400' : 'bg-rose-400'" class="w-1.5 h-1.5 rounded-full inline-block"></span>
                {{ backend.online ? 'Online' : 'Offline' }}
              </span>
            </div>
            <div class="text-xs text-slate-500 break-all font-mono">{{ backend.endpoint }}</div>
            <div class="text-xs text-slate-400">Agents: {{ backend.agents.join(', ') }}</div>
            <div class="text-xs text-slate-400">Models: {{ backend.model_count }}</div>
            <div v-if="backend.models_detailed?.length" class="flex flex-wrap gap-1 pt-1">
              <span
                v-for="model in backend.models_detailed.slice(0, 6)"
                :key="model.name || model.id"
                class="text-[10px] px-2 py-0.5 rounded-full bg-slate-700/80 text-slate-300 border border-cyan-500/20"
              >
                {{ formatModelLabel(model) }}
              </span>
            </div>
            <div v-else-if="backend.models?.length" class="text-[10px] text-slate-500 break-words font-mono">
              {{ backend.models.slice(0, 6).join(', ') }}
            </div>
            <div v-if="backend.probe_error" class="text-[10px] text-amber-400/80">
              {{ backend.probe_error }}
            </div>
          </div>

          <div class="space-y-1">
            <div
              v-for="agent in localAgents"
              :key="agent.name"
              class="text-xs flex items-center justify-between gap-2 px-2 py-1 rounded bg-slate-800/40"
            >
              <span class="text-slate-300 truncate font-mono">{{ agent.name }}</span>
              <span :class="agent.available_for_execution ? 'text-emerald-400' : 'text-slate-500'">
                {{ agent.available_for_execution ? 'ready' : 'not-ready' }}
              </span>
            </div>
          </div>
        </div>
        <p v-else class="text-xs text-slate-500 italic">
          No local model backends configured.
        </p>
      </div>

      <!-- Live Progress Logs -->
      <div v-if="store.isRunning" class="pt-4 border-t border-slate-700/60">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-xs font-semibold text-slate-300 uppercase tracking-wider">Live Progress</h3>
          <span class="text-xs text-amber-400 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse inline-block"></span>
            Running
          </span>
        </div>
        <div
          v-if="store.hasLogs"
          class="bg-slate-950 rounded-lg p-3 max-h-40 overflow-y-auto font-mono text-xs border border-slate-700/50"
        >
          <div
            v-for="log in store.logs.slice(-5)"
            :key="log.id"
            :class="{
              'text-blue-400': log.level === 'info',
              'text-emerald-400': log.level === 'success',
              'text-amber-400': log.level === 'warn' || log.level === 'warning',
              'text-red-400': log.level === 'error',
              'text-slate-400': !['info', 'success', 'warn', 'warning', 'error'].includes(log.level)
            }"
            class="mb-1 leading-relaxed truncate"
          >
            {{ log.message }}
          </div>
        </div>
        <p v-if="store.hasLogs" class="mt-1.5 text-xs text-slate-500 text-center">
          See Logs tab for full output
        </p>
        <p v-else class="mt-1.5 text-xs text-slate-500 text-center italic">
          Waiting for execution logs...
        </p>
      </div>

      <!-- Files Created: Tree View -->
      <div v-if="store.hasFiles" class="pt-4 border-t border-slate-700/60">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Generated Files
            <span class="ml-1 text-violet-400">({{ store.files.filter(f => !f.includes('__pycache__') && !f.endsWith('.pyc')).length }})</span>
          </h3>
          <span class="text-[10px] text-slate-500">Click to open</span>
        </div>
        <div class="max-h-56 overflow-y-auto rounded-lg bg-slate-950/50 border border-slate-800">
          <template v-for="node in sidebarFileTree" :key="node.path">
            <!-- Directory -->
            <div v-if="node.isDir">
              <button
                @click="node.open = !node.open"
                class="w-full text-left px-2 py-1 text-[11px] text-slate-400 hover:text-slate-200 flex items-center gap-1 transition-colors hover:bg-slate-800/40"
              >
                <span class="text-slate-600 text-[9px] w-3 flex-shrink-0">{{ node.open ? '&#9660;' : '&#9654;' }}</span>
                <span class="text-amber-500/70 flex-shrink-0">{{ node.open ? '&#128194;' : '&#128193;' }}</span>
                <span class="font-mono truncate">{{ node.name }}</span>
              </button>
              <div v-show="node.open">
                <button
                  v-for="child in node.children"
                  :key="child.path"
                  @click="openFileFromSidebar(child.path)"
                  class="w-full text-left pl-6 pr-2 py-1 text-[11px] text-slate-400 hover:text-cyan-300 hover:bg-cyan-500/10 flex items-center gap-1 transition-colors"
                >
                  <span class="flex-shrink-0">{{ sidebarFileIcon(child.name) }}</span>
                  <span class="font-mono truncate">{{ child.name }}</span>
                </button>
              </div>
            </div>
            <!-- Root-level file -->
            <button
              v-else
              @click="openFileFromSidebar(node.path)"
              class="w-full text-left px-2 py-1 text-[11px] text-slate-400 hover:text-cyan-300 hover:bg-cyan-500/10 flex items-center gap-1 transition-colors"
            >
              <span class="w-3 flex-shrink-0"></span>
              <span class="flex-shrink-0">{{ sidebarFileIcon(node.name) }}</span>
              <span class="font-mono truncate">{{ node.name }}</span>
            </button>
          </template>
        </div>
      </div>

    </div>
  </aside>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useOrchestratorStore } from '../stores/orchestrator'

const store = useOrchestratorStore()
const followUpInput = ref('')
const conversationMode = ref(false)

// File attachment for context injection
const fileInputRef = ref(null)
const attachedFileName = ref('')

const clearAttachment = () => {
  attachedFileName.value = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
}

const handleFileUpload = (event) => {
  const file = event.target.files?.[0]
  if (!file) return
  const ext = file.name.split('.').pop()?.toLowerCase()
  if (ext === 'pdf') {
    // PDF: inject filename hint; full text extraction requires pdfjs-dist
    attachedFileName.value = file.name
    const hint = `\n\n[Attached PDF: ${file.name} — paste key sections below for context]\n`
    store.task = (store.task || '').trimEnd() + hint
    if (fileInputRef.value) fileInputRef.value.value = ''
    return
  }
  const reader = new FileReader()
  reader.onload = (e) => {
    const content = e.target?.result || ''
    attachedFileName.value = file.name
    const header = `\n\n--- Context from ${file.name} ---\n`
    const footer = `\n--- End of ${file.name} ---\n`
    store.task = (store.task || '').trimEnd() + header + content.trim() + footer
  }
  reader.readAsText(file, 'utf-8')
  if (fileInputRef.value) fileInputRef.value.value = ''
}
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

const fileIcon = (name) => {
  const ext = name?.split('.').pop()?.toLowerCase()
  const icons = {
    py: '🐍', js: '📜', ts: '📘', json: '📋', yaml: '⚙️', yml: '⚙️',
    md: '📝', html: '🌐', css: '🎨', sh: '🔧', txt: '📄',
  }
  return icons[ext] || '📄'
}

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

watch(() => store.canFollowUp, (canFollowUp) => {
  if (canFollowUp && !conversationMode.value) {
    // Don't auto-enable, let user choose
  }
})

const handleExecute = () => {
  if (conversationMode.value && store.canFollowUp) {
    store.executeFollowUp(store.task)
  } else {
    store.executeTask()
    conversationMode.value = false
  }
}

const handleFollowUp = () => {
  if (followUpInput.value.trim()) {
    store.executeFollowUp(followUpInput.value)
    followUpInput.value = ''
  }
}

const handleCancel = async () => {
  try {
    const axios = (await import('axios')).default
    await axios.post('/api/cancel', { client_id: store.clientId })
  } catch (e) {
    console.error('Cancel failed:', e)
  }
}

// Agent dynamic status derived from agentActivity store
const AGENT_STATUS_MAP = {
  thinking:  { label: 'thinking',  textColor: 'text-amber-400',   spinColor: 'text-amber-400' },
  coding:    { label: 'coding',    textColor: 'text-cyan-400',    spinColor: 'text-cyan-400' },
  testing:   { label: 'testing',   textColor: 'text-blue-400',    spinColor: 'text-blue-400' },
  reviewing: { label: 'reviewing', textColor: 'text-violet-400',  spinColor: 'text-violet-400' },
  done:      { label: 'done',      textColor: 'text-emerald-400', spinColor: 'text-emerald-400' },
  error:     { label: 'error',     textColor: 'text-red-400',     spinColor: 'text-red-400' },
  idle:      { label: 'idle',      textColor: 'text-slate-500',   spinColor: 'text-slate-500' },
}

const agentRunStatus = (agentName) => {
  if (!store.isRunning) return AGENT_STATUS_MAP.idle
  const activity = store.agentActivity?.[agentName.toLowerCase()]
  if (!activity) return { label: 'idle', textColor: 'text-slate-600', spinColor: 'text-slate-600' }
  return AGENT_STATUS_MAP[activity.status] || AGENT_STATUS_MAP.thinking
}

// Sidebar File Tree — build collapsible tree from flat file list
const sidebarFileTree = computed(() => {
  const files = (store.files || []).filter(f =>
    !f.includes('__pycache__') && !f.endsWith('.pyc')
  )
  if (!files.length) return []

  // strip common prefix
  const parts = files.map(f => f.replace(/\\/g, '/').split('/'))
  let prefixLen = 0
  if (parts.length > 1) {
    const first = parts[0]
    outer: for (let i = 0; i < first.length; i++) {
      for (const p of parts) { if (p[i] !== first[i]) break outer }
      prefixLen = i + 1
    }
  } else if (parts.length === 1 && parts[0].length > 1) {
    prefixLen = parts[0].length - 1
  }

  const dirsMap = {}
  const rootFiles = []

  for (const fullPath of files) {
    const normalized = fullPath.replace(/\\/g, '/')
    const rel = normalized.split('/').slice(prefixLen).join('/')
    const segs = rel.split('/')
    if (segs.length === 1) {
      rootFiles.push({ name: segs[0], path: fullPath, isDir: false })
    } else {
      const dir = segs[0]
      if (!dirsMap[dir]) {
        dirsMap[dir] = reactive({ name: dir, isDir: true, open: true, children: [], path: dir })
      }
      dirsMap[dir].children.push({ name: segs.slice(1).join('/'), path: fullPath })
    }
  }
  return [...Object.values(dirsMap), ...rootFiles]
})

const sidebarFileIcon = (name) => {
  const ext = name?.split('.').pop()?.toLowerCase()
  const icons = {
    py: '🐍', js: '📜', ts: '📘', json: '📋', yaml: '⚙️', yml: '⚙️',
    md: '📝', html: '🌐', css: '🎨', sh: '🔧', txt: '📄',
    vue: '💚', jsx: '⚛️', tsx: '⚛️', rs: '🦀', go: '🐹',
  }
  return icons[ext] || '📄'
}

const openFileFromSidebar = (path) => {
  store.loadFile(path)
}
</script>
