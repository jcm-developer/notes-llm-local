<script setup>
import { ref, watch, computed } from "vue"
import Fonts from '../components/Fonts.vue'
import Chat from '../components/Chat.vue'
import Chats from '../components/Chats.vue'

const conversations = ref([])
const activeId = ref(null)

// cargar de localStorage
const saved = localStorage.getItem("conversations")
if (saved) {
    conversations.value = JSON.parse(saved)
    if (conversations.value.length) {
        activeId.value = conversations.value[0].id
    }
}

// guardar en localStorage
watch(conversations, (val) => {
    localStorage.setItem("conversations", JSON.stringify(val))
}, { deep: true })

const activeConversation = computed(() =>
    conversations.value.find(c => c.id === activeId.value)
)

// nueva conversación
const newConversation = () => {
    const id = crypto.randomUUID()
    const conv = { id, title: `Conversación ${conversations.value.length + 1}`, messages: [] }
    conversations.value.unshift(conv)
    activeId.value = id
}

// eliminar conversación
const deleteConversation = (id) => {
    const idx = conversations.value.findIndex(c => c.id === id)
    if (idx !== -1) {
        conversations.value.splice(idx, 1)
        // si era la activa, activar la primera disponible
        if (activeId.value === id) {
            activeId.value = conversations.value.length ? conversations.value[0].id : null
        }
    }
}

// renombrar conversación
const renameConversation = (id, newTitle) => {
    const conv = conversations.value.find(c => c.id === id)
    if (conv) conv.title = newTitle
}
</script>

<template>
    <br>
    <h1>> Notes-LLM Local</h1>
    <div class="main">
        <Fonts />
        <Chat v-if="activeConversation" :conversation="activeConversation" />
        <Chats :conversations="conversations" :active-id="activeId" @select="activeId = $event" @new="newConversation"
            @delete="deleteConversation" @rename="renameConversation" />
    </div>
</template>


<style scoped>
h1 {
    margin: 10px 0 10px 20px;
}
</style>
