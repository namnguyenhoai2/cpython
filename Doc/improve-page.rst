:orphan:

****************************
Cải thiện một trang tài liệu
****************************

.. This is the JavaScript-enabled version of this page. Another version
   (for those with JavaScript disabled) is improve-page-nojs.rst. If you
   edit this page, please also edit that one, and vice versa.

.. only:: html and not epub

   .. raw:: html

      <script>
         function applyReplacements(text, params) {
            return text
               .replace(/PAGETITLE/g, params.get('pagetitle'))
               .replace(/PAGEURL/g, params.get('pageurl'))
               .replace(/PAGESOURCE/g, params.get('pagesource'));
         }

         document.addEventListener('DOMContentLoaded', () => {
            const params = new URLSearchParams(window.location.search);
            const walker = document.createTreeWalker(
               document.body,
               NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
               null
            );

            while (walker.nextNode()) {
               const node = walker.currentNode;

               if (node.nodeType === Node.TEXT_NODE) {
                  node.textContent = applyReplacements(node.textContent, params)
               } else if (node.nodeName === 'A' && node.href) {
                  node.setAttribute('href', applyReplacements(node.getAttribute('href'), params));
               }
            }
         });
      </script>

Chúng tôi luôn sẵn lòng lắng nghe các ý tưởng về việc cải thiện tài liệu.

Bạn đang đọc "PAGETITLE" tại ` <PAGEURL>`_. Mã nguồn của trang đó nằm trên `GitHub <https://github.com/python/cpython/blob/main/Doc/PAGESOURCE?plain=1>`_.

.. only:: translation

   Nếu lỗi hoặc đề xuất cải thiện liên quan đến bản dịch của tài liệu này, thay vào đó hãy mở một issue hoặc chỉnh sửa trang trong `repository bản dịch <TRANSLATION_REPO_>`_.

Bạn có một vài cách để đặt câu hỏi hoặc đề xuất thay đổi:

- Bạn có thể bắt đầu một cuộc thảo luận về trang này trên diễn đàn thảo luận Python. Liên kết này sẽ bắt đầu một chủ đề được điền sẵn: `Câu hỏi về trang "PAGETITLE" <https://discuss.python.org/new-topic?category=documentation&title=Question+about+page+%22PAGETITLE%22&body=About+the+page+at+PAGEURL%3A>`_.

- Bạn có thể mở một issue trên trình theo dõi issue GitHub của Python. Liên kết này sẽ tạo một issue mới được điền sẵn: `Tài liệu: vấn đề với trang "PAGETITLE" <https://github.com/python/cpython/issues/new?template=documentation.yml&title=Docs%3A+problem+with+page+%22PAGETITLE%22&description=The+page+at+PAGEURL+has+a+problem%3A>`_.

- Bạn có thể `chỉnh sửa trang trên GitHub <https://github.com/python/cpython/blob/main/Doc/PAGESOURCE?plain=1>`_ để mở một pull request và bắt đầu quy trình đóng góp.

.. _`GitHub`: https://github.com/python/cpython/blob/main/Doc/PAGESOURCE?plain=1
.. _`translation's repository`: TRANSLATION_REPO_
.. _`Question about page "PAGETITLE"`: https://discuss.python.org/new-topic?category=documentation&title=Question+about+page+%22PAGETITLE%22&body=About+the+page+at+PAGEURL%3A
.. _`Docs: problem with page "PAGETITLE"`: https://github.com/python/cpython/issues/new?template=documentation.yml&title=Docs%3A+problem+with+page+%22PAGETITLE%22&description=The+page+at+PAGEURL+has+a+problem%3A
.. _`edit the page on GitHub`: https://github.com/python/cpython/blob/main/Doc/PAGESOURCE?plain=1
