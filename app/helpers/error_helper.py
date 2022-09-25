from enum import IntEnum


class ErrorCode(IntEnum):
    def __new__(cls, value, phrase, message=""):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.message = message
        return obj

    none = 0, "no error", "İşlem başarılı."
    error = 10000, "error", "Bir hata oluştu."
    invalid_access_token = 10001, "Geçersiz erişim tokeni."
    invalid_access_session = 10002, "Geçersiz oturum."
    invalid_permission = 10003, "Yetkisiz işlem."

    # Auth Errors
    invalid_email_verification_exp_date = 10100, "E-mail doğrulama süresi geçerli değil."
    invalid_email_verification_code = 10101, "E-mail doğrulama kodu geçersiz."

    # User Errors
    user_not_found = 10200, "Kullanıcı bulunamadı."
    inactive_user = 10201, "Kullanıcı aktif değil."
    user_already_exists = 10202, "Kullanıcı zaten mevcut."

    # Board Errors
    board_not_found = 10300, "Pano bulunamadı."
    board_not_active = 10301, "Pano arşivlenmiş, aktif değil."
    board_already_exists = 10302, "Pano zaten mevcut."
    user_not_member_the_board = 10303, "Kullanıcı pano üyesi değil."
    user_not_owner_the_board = 10304, "Kullanıcı pano yöneticisi değil."
    board_already_deleted = 10305, "Pano zaten silinmiş."
    user_already_exists_in_board = 10306, "Kullanıcı zaten pano üyesi."
    card_not_found = 10307, "Kart bulunamadı"
