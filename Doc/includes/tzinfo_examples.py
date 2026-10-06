import datetime as dt

# Lớp thể hiện khái niệm giờ địa phương của nền tảng.
# (Có thể cho giá trị sai với thời điểm lịch sử tại các múi giờ có
#  độ lệch UTC và/hoặc quy tắc DST đã thay đổi trong quá khứ.)
import time

ZERO = dt.timedelta(0)
HOUR = dt.timedelta(hours=1)
SECOND = dt.timedelta(seconds=1)

STDOFFSET = dt.timedelta(seconds=-time.timezone)
if time.daylight:
    DSTOFFSET = dt.timedelta(seconds=-time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET


class LocalTimezone(dt.tzinfo):

    def fromutc(self, when):
        assert when.tzinfo is self
        stamp = (when - dt.datetime(1970, 1, 1, tzinfo=self)) // SECOND
        args = time.localtime(stamp)[:6]
        dst_diff = DSTDIFF // SECOND
        # Phát hiện fold
        fold = (args == time.localtime(stamp - dst_diff))
        return dt.datetime(*args, microsecond=when.microsecond,
                           tzinfo=self, fold=fold)

    def utcoffset(self, when):
        if self._isdst(when):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, when):
        if self._isdst(when):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, when):
        return time.tzname[self._isdst(when)]

    def _isdst(self, when):
        tt = (when.year, when.month, when.day,
              when.hour, when.minute, when.second,
              when.weekday(), 0, 0)
        stamp = time.mktime(tt)
        tt = time.localtime(stamp)
        return tt.tm_isdst > 0


Local = LocalTimezone()


# Bản triển khai đầy đủ quy tắc DST hiện hành cho các múi giờ chính tại Hoa Kỳ.

def first_sunday_on_or_after(when):
    days_to_go = 6 - when.weekday()
    if days_to_go:
        when += dt.timedelta(days_to_go)
    return when


# Quy tắc DST tại Hoa Kỳ
#
# Đây là bộ quy tắc đơn giản hóa (nghĩa là sai trong vài trường hợp) cho thời
# điểm bắt đầu và kết thúc DST tại Hoa Kỳ. Để xem bộ quy tắc DST và định nghĩa
# múi giờ đầy đủ, cập nhật, hãy truy cập Cơ sở dữ liệu Olson (hoặc thử pytz):
# http://www.twinsun.com/tz/tz-link.htm
# https://sourceforge.net/projects/pytz/ (có thể không được cập nhật)
#
# Tại Hoa Kỳ, từ năm 2007, DST bắt đầu lúc 2 giờ sáng (giờ chuẩn) vào Chủ nhật
# thứ hai của tháng Ba, tức Chủ nhật đầu tiên vào hoặc sau ngày 8 tháng Ba.
DSTSTART_2007 = dt.datetime(1, 3, 8, 2)
# và kết thúc lúc 2 giờ sáng (giờ DST) vào Chủ nhật đầu tiên của tháng Mười Một.
DSTEND_2007 = dt.datetime(1, 11, 1, 2)
# Từ năm 1987 đến 2006, DST từng bắt đầu lúc 2 giờ sáng (giờ chuẩn) vào Chủ nhật
# đầu tiên của tháng Tư và kết thúc lúc 2 giờ sáng (giờ DST) vào Chủ nhật cuối
# cùng của tháng Mười, tức Chủ nhật đầu tiên vào hoặc sau ngày 25 tháng Mười.
DSTSTART_1987_2006 = dt.datetime(1, 4, 1, 2)
DSTEND_1987_2006 = dt.datetime(1, 10, 25, 2)
# Từ năm 1967 đến 1986, DST từng bắt đầu lúc 2 giờ sáng (giờ chuẩn) vào Chủ nhật
# cuối cùng của tháng Tư (vào hoặc sau ngày 24 tháng Tư) và kết thúc lúc 2 giờ
# sáng (giờ DST) vào Chủ nhật cuối cùng của tháng Mười, tức Chủ nhật đầu tiên
# vào hoặc sau ngày 25 tháng Mười.
DSTSTART_1967_1986 = dt.datetime(1, 4, 24, 2)
DSTEND_1967_1986 = DSTEND_1987_2006


def us_dst_range(year):
    # Tìm thời điểm bắt đầu và kết thúc DST tại Hoa Kỳ. Với năm trước 1967,
    # trả về start = end để biểu thị không có DST.
    if 2006 < year:
        dststart, dstend = DSTSTART_2007, DSTEND_2007
    elif 1986 < year < 2007:
        dststart, dstend = DSTSTART_1987_2006, DSTEND_1987_2006
    elif 1966 < year < 1987:
        dststart, dstend = DSTSTART_1967_1986, DSTEND_1967_1986
    else:
        return (dt.datetime(year, 1, 1), ) * 2

    start = first_sunday_on_or_after(dststart.replace(year=year))
    end = first_sunday_on_or_after(dstend.replace(year=year))
    return start, end


class USTimeZone(dt.tzinfo):

    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = dt.timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, when):
        if self.dst(when):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, when):
        return self.stdoffset + self.dst(when)

    def dst(self, when):
        if when is None or when.tzinfo is None:
            # Có thể hợp lý khi phát sinh ngoại lệ ở một hoặc cả hai trường hợp.
            # Điều đó tùy thuộc cách bạn muốn xử lý chúng. Bản triển khai mặc
            # định của fromutc() (được astimezone() mặc định gọi) truyền một
            # datetime có when.tzinfo là self.
            return ZERO
        assert when.tzinfo is self
        start, end = us_dst_range(when.year)
        # Không thể so sánh đối tượng ngây thơ với đối tượng nhận biết múi giờ,
        # nên trước hết hãy bỏ múi giờ khỏi when.
        when = when.replace(tzinfo=None)
        if start + HOUR <= when < end - HOUR:
            # DST đang có hiệu lực.
            return HOUR
        if end - HOUR <= when < end:
            # Fold (một giờ mơ hồ): dùng when.fold để phân biệt.
            return ZERO if when.fold else HOUR
        if start <= when < start + HOUR:
            # Gap (một giờ không tồn tại): đảo ngược quy tắc fold.
            return HOUR if when.fold else ZERO
        # DST không có hiệu lực.
        return ZERO

    def fromutc(self, when):
        assert when.tzinfo is self
        start, end = us_dst_range(when.year)
        start = start.replace(tzinfo=self)
        end = end.replace(tzinfo=self)
        std_time = when + self.stdoffset
        dst_time = std_time + HOUR
        if end <= dst_time < end + HOUR:
            # Giờ lặp lại
            return std_time.replace(fold=1)
        if std_time < start or dst_time >= end:
            # Giờ chuẩn
            return std_time
        if start <= std_time < end - HOUR:
            # Giờ mùa hè
            return dst_time


Eastern  = USTimeZone(-5, "Eastern",  "EST", "EDT")
Central  = USTimeZone(-6, "Central",  "CST", "CDT")
Mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
Pacific  = USTimeZone(-8, "Pacific",  "PST", "PDT")
