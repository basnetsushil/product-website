document.addEventListener('DOMContentLoaded', () => {
    // Chatbot Toggle Logic
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    chatToggle.addEventListener('click', () => chatWindow.classList.toggle('hidden'));
    chatClose.addEventListener('click', () => chatWindow.classList.add('hidden'));

    // Keyword-based Chatbot Responses
    const responses = {
        "hello": "Hello! 👋 Welcome to AI-Solutions. How can I help you transform your business today?",
        "hi": "Hi there! I'm the AI-Solutions assistant. What's on your mind?",
        "solutions": "We offer a wide range of AI services including Machine Learning, Predictive Analytics, and custom LLM implementations. Check our /solutions page!",
        "services": "Our core services include AI Strategy, Automation, and Data Engineering. Would you like to see our portfolio?",
        "contact": "You can reach us via our Contact page or email us directly at contact@ai-solutions.co.uk",
        "about": "AI-Solutions is a premier AI consultancy based in Sunderland, UK, focusing on enterprise-grade automation.",
        "company": "We are a team of AI researchers and engineers dedicated to solving real-world business problems.",
        "pricing": "Our pricing is tailored to your specific needs. Please contact our sales team for a custom quote.",
        "case studies": "We've helped dozens of companies scale. Visit our Case Studies page to see the results!",
        "events": "We host monthly AI workshops in Sunderland. Check the Events page for upcoming dates.",
        "articles": "Our blog is full of insights on the future of AI. Head over to the Insights section!",
        "blog": "Check out our articles page for the latest in AI research and trends.",
        "team": "Our team consists of world-class engineers and AI strategists. Meet them on our Team page."
    };

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = chatInput.value.toLowerCase().trim();
        if (!query) return;

        // User message
        appendMessage(chatInput.value, 'user');
        chatInput.value = '';

        // Bot response delay
        setTimeout(() => {
            let response = "I'm not sure I understand. Could you please contact our human support team via the contact page? 😊";
            
            for (let key in responses) {
                if (query.includes(key)) {
                    response = responses[key];
                    break;
                }
            }
            appendMessage(response, 'bot');
        }, 600);
    });

    function appendMessage(text, sender) {
        const div = document.createElement('div');
        div.className = sender === 'user' 
            ? "bg-white/20 p-3 rounded-lg rounded-tr-none max-w-[80%] ml-auto text-right text-white" 
            : "bg-white/10 p-3 rounded-lg rounded-tl-none max-w-[80%] text-neutral-300";
        div.textContent = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});