import { onMounted, onUpdated } from 'vue'
import { copyText } from '@/utils/format'

export function useCopyCode() {
  copyCodeBlock()

  onMounted(() => copyCodeBlock())

  // !UNDELETED 不会被触发，移动端下有触发情况
  onUpdated(() => {
    copyCodeBlock()
  })
}

export function copyCodeBlock() {
  const codeBlockWrapper = document.querySelectorAll('.code-block-wrapper')
  codeBlockWrapper.forEach((wrapper) => {
    const copyBtn = wrapper.querySelector('.code-block-header__copy')
    const codeBlock = wrapper.querySelector('.code-block-body')
    if (copyBtn && codeBlock) {
      copyBtn.addEventListener('click', () => {
        if (navigator.clipboard?.writeText)
          navigator.clipboard.writeText(codeBlock.textContent ?? '')
        else
          copyText({ text: codeBlock.textContent ?? '', origin: true })
      })
    }
  })
}