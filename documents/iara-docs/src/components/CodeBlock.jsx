import { useState } from 'react'
import { Copy, Check } from 'lucide-react'

const CodeBlock = ({ code, language = 'json', title }) => {
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  const highlightCode = (code, lang) => {
    // Simple syntax highlighting for JSON and JavaScript
    if (lang === 'json') {
      return code
        .replace(/"([^"]+)":/g, '<span class="text-blue-400">"$1"</span>:')
        .replace(/: "([^"]+)"/g, ': <span class="text-green-400">"$1"</span>')
        .replace(/: (\d+)/g, ': <span class="text-orange-400">$1</span>')
        .replace(/: (true|false|null)/g, ': <span class="text-purple-400">$1</span>')
    }
    
    if (lang === 'javascript') {
      return code
        .replace(/(const|let|var|function|return|import|from|export|default)/g, '<span class="text-purple-400">$1</span>')
        .replace(/"([^"]+)"/g, '<span class="text-green-400">"$1"</span>')
        .replace(/\/\/.*$/gm, '<span class="text-gray-500">$&</span>')
    }

    if (lang === 'bash' || lang === 'shell') {
      return code
        .replace(/^(GET|POST|PUT|DELETE|PATCH)/gm, '<span class="text-blue-400">$1</span>')
        .replace(/https?:\/\/[^\s]+/g, '<span class="text-green-400">$&</span>')
    }

    return code
  }

  return (
    <div className="relative group">
      {title && (
        <div className="bg-gray-800 px-4 py-2 text-sm text-gray-300 border-b border-gray-700 rounded-t-lg">
          {title}
        </div>
      )}
      <div className="relative bg-gray-900 rounded-lg overflow-hidden">
        <button
          onClick={copyToClipboard}
          className="absolute top-3 right-3 p-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
          title="Copiar código"
        >
          {copied ? (
            <Check className="w-4 h-4 text-green-400" />
          ) : (
            <Copy className="w-4 h-4 text-gray-400" />
          )}
        </button>
        <pre className="p-4 text-sm text-gray-300 overflow-x-auto">
          <code
            dangerouslySetInnerHTML={{
              __html: highlightCode(code, language)
            }}
          />
        </pre>
      </div>
    </div>
  )
}

export default CodeBlock

