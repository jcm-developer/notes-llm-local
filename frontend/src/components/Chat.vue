<script setup>
import { ref } from "vue"

const props = defineProps({
    conversation: Object
})
const inputText = ref("")

const sendMessage = async () => {
    if (!inputText.value.trim()) return

    props.conversation.messages.push({ role: "user", content: inputText.value })
    const myMessage = inputText.value
    inputText.value = ""

    try {
        const formData = new FormData()
        formData.append("question", myMessage)

        const res = await fetch("http://localhost:8001/query", {
            method: "POST",
            body: formData,
        })
        const data = await res.json()

        props.conversation.messages.push({ role: "assistant", content: data.answer })

        // renombrar la conversación con el primer mensaje si no tiene título
        if (props.conversation.title.startsWith("Conversación") && props.conversation.messages.length === 2) {
            props.conversation.title = myMessage.slice(0, 30) + "..."
        }
    } catch (err) {
        props.conversation.messages.push({ role: "assistant", content: "⚠️ Error al consultar el LLM" })
    }
}
</script>

<template>
    <div class="panel chat-panel">
        <h2>Chat</h2>
        <hr />

        <!-- cuerpo de chat -->
        <div class="chat-body">
            <div v-for="(msg, i) in conversation.messages" :key="i" class="chat-message" :class="msg.role">
                <p style="font-size: 14px;">{{ msg.content }}</p>
            </div>
        </div>

        <!-- barra de entrada -->
        <div class="buttons">
            <input v-model="inputText" type="text" class="chat-input" placeholder="Escribe un mensaje..."
                @keyup.enter="sendMessage" />
            <button class="button" @click="sendMessage">Enviar</button>
        </div>
    </div>
</template>

<style scoped>
.chat-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.chat-body {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-message {
    max-width: 70%;
    padding: 10px 14px;
    border-radius: 8px;
    word-wrap: break-word;
    white-space: pre-wrap;
    line-height: 1.4;
}

.chat-message.user {
    align-self: flex-end;
    background: #272c31;
    color: #e5e7eb;
}

.chat-message.assistant {
    align-self: flex-start;
    background: transparent;
    color: #e5e7eb;
}

.buttons {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
}

.buttons input {
    flex: 1;
    padding: 16px;
}

.buttons button {
    width: 15%;
    padding: 16px;
}
</style>
