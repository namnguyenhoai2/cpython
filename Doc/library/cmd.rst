:mod:`!cmd` --- Hỗ trợ trình thông dịch lệnh theo dòng
======================================================

.. module:: cmd
   :synopsis: Xây dựng trình thông dịch lệnh theo dòng.

.. sectionauthor:: Eric S. Raymond <esr@snark.thyrsus.com>

**Mã nguồn:** :source:`Lib/cmd.py`

--------------

Lớp :class:`Cmd` cung cấp một framework đơn giản để viết các trình thông dịch lệnh theo dòng. Những trình thông dịch này thường hữu ích cho các bộ kiểm thử, công cụ quản trị và nguyên mẫu mà sau này sẽ được bọc trong một giao diện tinh vi hơn.

.. class:: Cmd(completekey='tab', stdin=None, stdout=None)

   Một đối tượng :class:`Cmd` hoặc một thể hiện của lớp con là một framework trình thông dịch theo dòng. Không có lý do chính đáng để tự khởi tạo :class:`Cmd`; thay vào đó, lớp này hữu ích khi làm lớp cha của một lớp trình thông dịch do bạn tự định nghĩa, nhằm kế thừa các phương thức của :class:`Cmd` và đóng gói các phương thức hành động.

   Đối số tùy chọn *completekey* là tên :mod:`readline` của một phím hoàn tất; mặc định là :kbd:`Tab`. Nếu *completekey* không phải là :const:`None` và
   :mod:`readline` khả dụng, việc hoàn tất lệnh sẽ được thực hiện tự động.

   Giá trị mặc định, ``'tab'``, được xử lý đặc biệt, nên nó tham chiếu đến
   khóa :kbd:`Tab` trên mọi :data:`readline.backend`. Cụ thể, nếu :data:`readline.backend` là ``editline``, ``Cmd`` sẽ sử dụng ``'^I'`` thay vì ``'tab'``. Lưu ý rằng các giá trị khác không được xử lý theo cách này và có thể chỉ hoạt động với một backend cụ thể.

   Các đối số tùy chọn *stdin* và *stdout* chỉ định các đối tượng tệp đầu vào và đầu ra mà instance Cmd hoặc instance lớp con sẽ sử dụng cho việc nhập và xuất. Nếu không được chỉ định, chúng sẽ mặc định là :data:`sys.stdin` và
   :data:`sys.stdout`.

   Nếu bạn muốn sử dụng một *stdin* cụ thể, hãy đảm bảo đặt thuộc tính của instance
   :attr:`use_rawinput` thành ``False``, nếu không *stdin* sẽ bị bỏ qua.

   .. versionchanged:: 3.13
      ``completekey='tab'`` được thay thế bằng ``'^I'`` cho ``editline``.


.. _cmd-objects:

Các đối tượng Cmd
-----------------

Một instance :class:`Cmd` có các phương thức sau:


.. method:: Cmd.cmdloop(intro=None)

   Liên tục hiển thị lời nhắc, nhận dữ liệu nhập, phân tích phần tiền tố ban đầu khỏi dữ liệu nhận được và phân phối đến các phương thức action, truyền phần còn lại của dòng làm đối số cho chúng.

   Đối số tùy chọn là một chuỗi banner hoặc lời giới thiệu được hiển thị trước lời nhắc đầu tiên (đối số này ghi đè thuộc tính lớp :attr:`intro`).

   Nếu module :mod:`readline` được tải, dữ liệu nhập sẽ tự động kế thừa
   tính năng chỉnh sửa danh sách lịch sử giống :program:`bash`\  (ví dụ: :kbd:`Control-P` cuộn về lệnh gần nhất, :kbd:`Control-N` chuyển tới lệnh tiếp theo, :kbd:`Control-F` di chuyển con trỏ sang phải mà không xóa nội dung, :kbd:`Control-B` di chuyển con trỏ sang trái mà không xóa nội dung, v.v.).

   Ký hiệu kết thúc tệp trong dữ liệu nhập được trả về dưới dạng chuỗi ``'EOF'``.

   .. index::
      single: ? (question mark); in a command interpreter
      single: ! (exclamation); in a command interpreter

   Một instance của interpreter sẽ nhận diện tên lệnh ``foo`` khi và chỉ khi nó có phương thức :meth:`!do_foo`. Trong trường hợp đặc biệt, một dòng bắt đầu bằng ký tự ``'?'`` sẽ được phân phối đến phương thức :meth:`do_help`. Trong một trường hợp đặc biệt khác, một dòng bắt đầu bằng ký tự ``'!'`` sẽ được phân phối đến phương thức :meth:`!do_shell` (nếu phương thức đó được định nghĩa).

   Phương thức này sẽ trả về khi phương thức :meth:`postcmd` trả về giá trị true. Đối số *stop* của :meth:`postcmd` là giá trị trả về từ phương thức :meth:`!do_\*` tương ứng của lệnh.

   Nếu tính năng hoàn tất được bật, các lệnh sẽ được hoàn tất tự động, còn việc hoàn tất các đối số của lệnh được thực hiện bằng cách gọi :meth:`!complete_foo` với các đối số *text*, *line*, *begidx* và *endidx*. *text* là tiền tố chuỗi mà chúng ta đang cố gắng khớp: mọi kết quả khớp được trả về đều phải bắt đầu bằng tiền tố này. *line* là dòng nhập hiện tại sau khi đã loại bỏ khoảng trắng ở đầu, còn *begidx* và *endidx* là các chỉ mục bắt đầu và kết thúc của phần văn bản tiền tố; có thể dùng chúng để cung cấp nội dung hoàn tất khác nhau tùy vào vị trí của đối số.


.. method:: Cmd.do_help(arg)

   Tất cả lớp con của :class:`Cmd` đều kế thừa một :meth:`!do_help` được định nghĩa sẵn. Phương thức này, khi được gọi với đối số ``'bar'``, sẽ gọi phương thức tương ứng
   :meth:`!help_bar`, và nếu phương thức đó không tồn tại thì in ra docstring của
   :meth:`!do_bar`, nếu có. Khi không có đối số, :meth:`!do_help` liệt kê tất cả chủ đề trợ giúp hiện có (tức là tất cả các lệnh có phương thức :meth:`!do_bar` tương ứng
   :meth:`!help_\*` hoặc các lệnh có docstring), đồng thời cũng liệt kê mọi lệnh không có tài liệu.


.. method:: Cmd.onecmd(str)

   Diễn giải đối số như thể nó được nhập để trả lời lời nhắc. Có thể ghi đè hành vi này, nhưng thông thường không cần làm vậy; xem
   Các phương thức :meth:`precmd` và :meth:`postcmd` cung cấp các hook thực thi hữu ích. Giá trị trả về là một cờ cho biết có nên dừng việc trình thông dịch diễn giải các lệnh hay không. Nếu có phương thức :meth:`!do_\*` cho lệnh *str*, giá trị trả về của phương thức đó sẽ được trả về; nếu không, giá trị trả về từ phương thức :meth:`default` sẽ được trả về.


.. method:: Cmd.emptyline()

   Phương thức được gọi khi người dùng nhập một dòng trống để phản hồi lời nhắc. Nếu phương thức này không được ghi đè, phương thức sẽ lặp lại lệnh không trống gần nhất đã nhập.


.. method:: Cmd.default(line)

   Phương thức được gọi trên một dòng đầu vào khi tiền tố lệnh không được nhận dạng. Nếu phương thức này không được ghi đè, phương thức sẽ in thông báo lỗi rồi trả về.


.. method:: Cmd.completedefault(text, line, begidx, endidx)

   Phương thức được gọi để hoàn tất một dòng đầu vào khi không có phương thức dành riêng cho lệnh nào
   :meth:`!complete_\*` khả dụng. Theo mặc định, phương thức này trả về một danh sách trống.


.. method:: Cmd.columnize(list, displaywidth=80)

   Phương thức được gọi để hiển thị danh sách chuỗi dưới dạng một tập hợp cột gọn. Mỗi cột chỉ rộng vừa đủ. Các cột được phân cách bằng hai khoảng trắng để dễ đọc.


.. method:: Cmd.precmd(line)

   Phương thức hook được thực thi ngay trước khi dòng lệnh *line* được diễn giải, nhưng sau khi lời nhắc nhập liệu được tạo và hiển thị. Phương thức này là một stub trong
   :class:`Cmd`; nó tồn tại để được ghi đè bởi các lớp con. Giá trị trả về được sử dụng làm lệnh sẽ được thực thi bởi phương thức :meth:`onecmd`; giá trị
   Phần triển khai :meth:`precmd` có thể viết lại lệnh hoặc chỉ trả về *line* không thay đổi.


.. method:: Cmd.postcmd(stop, line)

   Phương thức hook được thực thi ngay sau khi quá trình điều phối lệnh kết thúc. Phương thức này là một stub trong :class:`Cmd`; nó tồn tại để được ghi đè bởi các lớp con. *line* là dòng lệnh đã được thực thi, còn *stop* là một cờ cho biết liệu quá trình thực thi có bị kết thúc sau lần gọi :meth:`postcmd` hay không; đây sẽ là giá trị trả về của phương thức :meth:`onecmd`. Giá trị trả về của phương thức này sẽ được sử dụng làm giá trị mới cho cờ nội bộ tương ứng với *stop*; trả về false sẽ khiến quá trình diễn giải tiếp tục.


.. method:: Cmd.preloop()

   Phương thức hook được thực thi một lần khi :meth:`cmdloop` được gọi. Phương thức này là một stub trong :class:`Cmd`; nó tồn tại để được ghi đè bởi các lớp con.


.. method:: Cmd.postloop()

   Phương thức hook được thực thi một lần ngay trước khi :meth:`cmdloop` trả về. Phương thức này là một stub trong :class:`Cmd`; nó tồn tại để được ghi đè bởi các lớp con.


Các instance của các lớp con :class:`Cmd` có một số biến instance công khai:

.. attribute:: Cmd.prompt

   Lời nhắc được đưa ra để yêu cầu nhập dữ liệu.


.. attribute:: Cmd.identchars

   Chuỗi ký tự được chấp nhận làm tiền tố lệnh.


.. attribute:: Cmd.lastcmd

   Tiền tố lệnh không rỗng cuối cùng được thấy.


.. attribute:: Cmd.cmdqueue

   Danh sách các dòng đầu vào đang chờ xử lý. Danh sách cmdqueue được kiểm tra trong
   :meth:`cmdloop` khi cần đầu vào mới; nếu danh sách này không rỗng, các phần tử của nó sẽ được xử lý theo thứ tự, như thể được nhập tại dấu nhắc.


.. attribute:: Cmd.intro

   Một chuỗi cần xuất dưới dạng lời giới thiệu hoặc banner. Có thể ghi đè bằng cách truyền
   :meth:`cmdloop` một đối số.


.. attribute:: Cmd.doc_header

   Tiêu đề cần xuất nếu phần trợ giúp có một mục dành cho các lệnh được lập tài liệu.


.. attribute:: Cmd.misc_header

   Tiêu đề cần hiển thị nếu đầu ra trợ giúp có một phần dành cho các chủ đề trợ giúp khác (tức là có các phương thức :meth:`!help_\*` không có phương thức tương ứng
   :meth:`!do_\*`).


.. attribute:: Cmd.undoc_header

   Tiêu đề cần hiển thị nếu đầu ra trợ giúp có một phần dành cho các lệnh chưa được ghi tài liệu (tức là có các phương thức :meth:`!do_\*` không có các phương thức :meth:`!help_\*` tương ứng).


.. attribute:: Cmd.ruler

   Ký tự dùng để vẽ các đường phân cách bên dưới tiêu đề thông báo trợ giúp. Nếu để trống, sẽ không vẽ đường kẻ. Giá trị mặc định là ``'='``.


.. attribute:: Cmd.use_rawinput

   Một cờ, mặc định là true. Nếu là true, :meth:`cmdloop` sử dụng :func:`input` để hiển thị lời nhắc và đọc lệnh tiếp theo; nếu là false, :data:`sys.stdout.write() <sys.stdout>` và :data:`sys.stdin.readline() <sys.stdin>` được sử dụng. (Điều này có nghĩa là bằng cách import
   :mod:`readline`, trên các hệ thống hỗ trợ tính năng này, trình thông dịch sẽ tự động hỗ trợ tính năng chỉnh sửa dòng giống :program:`Emacs`\  và các phím tắt lịch sử lệnh.)


.. _cmd-example:

Ví dụ về Cmd
------------

.. sectionauthor:: Raymond Hettinger <python at rcn dot com>

Mô-đun :mod:`!cmd` chủ yếu hữu ích để xây dựng các shell tùy chỉnh, cho phép người dùng tương tác với một chương trình.

Phần này trình bày một ví dụ đơn giản về cách xây dựng một shell bao quanh một vài lệnh trong mô-đun :mod:`turtle`.

Các lệnh turtle cơ bản như :meth:`~turtle.forward` được thêm vào một
lớp con :class:`Cmd` với phương thức có tên :meth:`!do_forward`. Đối số được chuyển đổi thành một số rồi chuyển tiếp đến mô-đun turtle. Docstring được sử dụng trong tiện ích trợ giúp do shell cung cấp.

Ví dụ cũng bao gồm một chức năng ghi và phát lại cơ bản được triển khai bằng phương thức :meth:`~Cmd.precmd`, chịu trách nhiệm chuyển đổi đầu vào thành chữ thường và ghi các lệnh vào một tệp. Phương thức :meth:`!do_playback` đọc tệp và thêm các lệnh đã ghi vào :attr:`~Cmd.cmdqueue` để phát lại ngay lập tức::

    import cmd, sys
    from turtle import *

    class TurtleShell(cmd.Cmd):
        intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
        prompt = '(turtle) '
        file = None

        # ----- các lệnh turtle cơ bản -----
        def do_forward(self, arg):
            'Move the turtle forward by the specified distance:  FORWARD 10'
            forward(*parse(arg))
        def do_right(self, arg):
            'Turn turtle right by given number of degrees:  RIGHT 20'
            right(*parse(arg))
        def do_left(self, arg):
            'Turn turtle left by given number of degrees:  LEFT 90'
            left(*parse(arg))
        def do_goto(self, arg):
            'Move turtle to an absolute position with changing orientation.  GOTO 100 200'
            goto(*parse(arg))
        def do_home(self, arg):
            'Return turtle to the home position:  HOME'
            home()
        def do_circle(self, arg):
            'Draw circle with given radius an options extent and steps:  CIRCLE 50'
            circle(*parse(arg))
        def do_position(self, arg):
            'Print the current turtle position:  POSITION'
            print('Current position is %d %d\n' % position())
        def do_heading(self, arg):
            'Print the current turtle heading in degrees:  HEADING'
            print('Current heading is %d\n' % (heading(),))
        def do_color(self, arg):
            'Set the color:  COLOR BLUE'
            color(arg.lower())
        def do_undo(self, arg):
            'Undo (repeatedly) the last turtle action(s):  UNDO'
        def do_reset(self, arg):
            'Clear the screen and return turtle to center:  RESET'
            reset()
        def do_bye(self, arg):
            'Stop recording, close the turtle window, and exit:  BYE'
            print('Thank you for using Turtle')
            self.close()
            bye()
            return True

        # ----- ghi và phát lại -----
        def do_record(self, arg):
            'Save future commands to filename:  RECORD rose.cmd'
            self.file = open(arg, 'w')
        def do_playback(self, arg):
            'Playback commands from a file:  PLAYBACK rose.cmd'
            self.close()
            with open(arg) as f:
                self.cmdqueue.extend(f.read().splitlines())
        def precmd(self, line):
            line = line.lower()
            if self.file and 'playback' not in line:
                print(line, file=self.file)
            return line
        def close(self):
            if self.file:
                self.file.close()
                self.file = None

    def parse(arg):
        'Convert a series of zero or more numbers to an argument tuple'
        return tuple(map(int, arg.split()))

    if __name__ == '__main__':
        TurtleShell().cmdloop()


Dưới đây là một phiên mẫu với turtle shell, trong đó trình bày các hàm trợ giúp, cách sử dụng dòng trống để lặp lại lệnh, cùng với tiện ích ghi và phát lại đơn giản:

.. code-block:: none

    Welcome to the turtle shell.   Type help or ? to list commands.

    (turtle) ?

    Documented commands (type help <topic>):
    ========================================
    bye     color    goto     home  playback  record  right
    circle  forward  heading  left  position  reset   undo

    (turtle) help forward
    Move the turtle forward by the specified distance:  FORWARD 10
    (turtle) record spiral.cmd
    (turtle) position
    Current position is 0 0

    (turtle) heading
    Current heading is 0

    (turtle) reset
    (turtle) circle 20
    (turtle) right 30
    (turtle) circle 40
    (turtle) right 30
    (turtle) circle 60
    (turtle) right 30
    (turtle) circle 80
    (turtle) right 30
    (turtle) circle 100
    (turtle) right 30
    (turtle) circle 120
    (turtle) right 30
    (turtle) circle 120
    (turtle) heading
    Current heading is 180

    (turtle) forward 100
    (turtle)
    (turtle) right 90
    (turtle) forward 100
    (turtle)
    (turtle) right 90
    (turtle) forward 400
    (turtle) right 90
    (turtle) forward 500
    (turtle) right 90
    (turtle) forward 400
    (turtle) right 90
    (turtle) forward 300
    (turtle) playback spiral.cmd
    Current position is 0 0

    Current heading is 0

    Current heading is 180

    (turtle) bye
    Thank you for using Turtle
