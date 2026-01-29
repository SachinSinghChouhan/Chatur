import { useRef } from 'react';
import { motion, useInView } from 'motion/react';

const englishExamples = [
  { user: 'Hey Chatur, what\'s the weather today?', chatur: 'It\'s 24 degrees and sunny in Delhi.' },
  { user: 'Open my presentation', chatur: 'Opening PowerPoint presentation from Documents.' },
  { user: 'Set a reminder for 3 PM', chatur: 'Reminder set for 3 PM today.' },
];

const hindiExamples = [
  { user: 'Chatur, aaj ka weather kaisa hai?', chatur: 'Aaj Delhi mein 24 degree hai aur dhoop khili hui hai.' },
  { user: 'Mere presentation ko kholo', chatur: 'Documents se PowerPoint presentation khol raha hoon.' },
  { user: 'Teen baje ka reminder set karo', chatur: 'Aaj 3 baje ka reminder set kar diya hai.' },
];

function ChatBubble({ text, isUser }: { text: string; isUser: boolean }) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className="max-w-xs px-4 py-3 rounded-lg"
        style={{
          backgroundColor: isUser ? 'var(--accent-primary)' : 'var(--surface-card)',
          color: 'var(--text-primary)',
          borderWidth: isUser ? '0' : '1px',
          borderColor: 'var(--surface-border)',
        }}
      >
        <p className="text-sm">{text}</p>
      </div>
    </div>
  );
}

export function BilingualDemo() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.1 });

  return (
    <section
      ref={ref}
      className="py-24 px-6"
      style={{ backgroundColor: 'var(--background-secondary)' }}
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4" style={{ color: 'var(--text-primary)' }}>
            Speak Your Language
          </h2>
          <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
            Natural conversations in English or Hindi
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* English Examples */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
            transition={{ duration: 0.5, delay: 0.2, ease: 'easeOut' }}
          >
            <h3 className="text-xl mb-6 text-center" style={{ color: 'var(--text-primary)' }}>
              English
            </h3>
            <div
              className="p-6 rounded-lg border"
              style={{
                backgroundColor: 'var(--background)',
                borderColor: 'var(--surface-border)',
              }}
            >
              {englishExamples.map((example, index) => (
                <div key={index}>
                  <ChatBubble text={example.user} isUser={true} />
                  <ChatBubble text={example.chatur} isUser={false} />
                </div>
              ))}
            </div>
          </motion.div>

          {/* Hindi Examples */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 20 }}
            transition={{ duration: 0.5, delay: 0.2, ease: 'easeOut' }}
          >
            <h3 className="text-xl mb-6 text-center" style={{ color: 'var(--text-primary)' }}>
              हिन्दी (Hindi)
            </h3>
            <div
              className="p-6 rounded-lg border"
              style={{
                backgroundColor: 'var(--background)',
                borderColor: 'var(--surface-border)',
              }}
            >
              {hindiExamples.map((example, index) => (
                <div key={index}>
                  <ChatBubble text={example.user} isUser={true} />
                  <ChatBubble text={example.chatur} isUser={false} />
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}