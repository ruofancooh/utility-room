#include <stdio.h>
#include <time.h>
#include <stdlib.h> //system("cls")
#include <conio.h> //_kbhit()

#define YANG 'O'
#define YIN ' '
#define ROW 7
#define COL 34

char matrix[ROW][COL] = {
    /*0                        5                                  12                       17                                 24                       29                  33*/
    {'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', '\n'},
    {'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', '\n'},
    {'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', '\n'},
    {'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', '\n'},
    {'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', '\n'},
    {'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', '\n'},
    {'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', '\0'}};

const int kColOffset[] = {0, 5, 12, 17, 24, 29};

char *pin[] = {&matrix[0][0], &matrix[0][1], &matrix[0][2], &matrix[0][3]};

#define pinMoveDown()  \
    {                  \
        pin[0] += COL; \
        pin[1] += COL; \
        pin[2] += COL; \
        pin[3] += COL; \
    }

#define pinReset()              \
    {                           \
        pin[0] = &matrix[0][0]; \
        pin[1] = &matrix[0][1]; \
        pin[2] = &matrix[0][2]; \
        pin[3] = &matrix[0][3]; \
    }

time_t utc_time;
struct tm local_time;
int h_1, h_2, m_1, m_2, s_1, s_2;

#define getTime()                            \
    {                                        \
        utc_time = time(NULL);               \
        localtime_s(&local_time, &utc_time); \
        h_1 = local_time.tm_hour / 10;       \
        h_2 = local_time.tm_hour % 10;       \
        m_1 = local_time.tm_min / 10;        \
        m_2 = local_time.tm_min % 10;        \
        s_1 = local_time.tm_sec / 10;        \
        s_2 = local_time.tm_sec % 10;        \
    }

#define saveTime2Matrix()               \
    {                                   \
        writeDigit(h_1, kColOffset[0]); \
        writeDigit(h_2, kColOffset[1]); \
        writeDigit(m_1, kColOffset[2]); \
        writeDigit(m_2, kColOffset[3]); \
        writeDigit(s_1, kColOffset[4]); \
        writeDigit(s_2, kColOffset[5]); \
    }

const int kDigitsRows[10][ROW];

void writeDigit(int digit, int offset)
{
    pin[0] += offset, pin[1] += offset, pin[2] += offset, pin[3] += offset;
    for (int row = 0; row < ROW; row++)
    {
        int write_type = kDigitsRows[digit][row];
        switch (write_type)
        {
        case 0b1111:
            *pin[0] = YANG;
            *pin[1] = YANG;
            *pin[2] = YANG;
            *pin[3] = YANG;
            break;
        case 0b0001:
            *pin[0] = YIN;
            *pin[1] = YIN;
            *pin[2] = YIN;
            *pin[3] = YANG;
            break;
        case 0b1001:
            *pin[0] = YANG;
            *pin[1] = YIN;
            *pin[2] = YIN;
            *pin[3] = YANG;
            break;
        case 0b1000:
            *pin[0] = YANG;
            *pin[1] = YIN;
            *pin[2] = YIN;
            *pin[3] = YIN;
            break;
        }
        pinMoveDown();
    }
    pinReset();
}

const int kDigitsRows[10][ROW] =
    {
        {0b1111, 0b1001, 0b1001, 0b1001, 0b1001, 0b1001, 0b1111},
        /* 0 1 2 3
        **********
        0| A A A A
        1| A     A
        2| A     A
        3| A     A
        4| A     A
        5| A     A
        6| A A A A
        **********/
        {0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001},
        /* 0 1 2 3
        **********
        0|       A
        1|       A
        2|       A
        3|       A
        4|       A
        5|       A
        6|       A
        **********/
        {0b1111, 0b0001, 0b0001, 0b1111, 0b1000, 0b1000, 0b1111},
        /* 0 1 2 3
        **********
        0| A A A A
        1|       A
        2|       A
        3| A A A A
        4| A
        5| A
        6| A A A A
        **********/
        {0b1111, 0b0001, 0b0001, 0b1111, 0b0001, 0b0001, 0b1111},
        /* 0 1 2 3
        **********
        0| A A A A
        1|       A
        2|       A
        3| A A A A
        4|       A
        5|       A
        6| A A A A
        **********/
        {0b1001, 0b1001, 0b1001, 0b1111, 0b0001, 0b0001, 0b0001},
        /* 0 1 2 3
        **********
        0| A     A
        1| A     A
        2| A     A
        3| A A A A
        4|       A
        5|       A
        6|       A
        **********/
        {0b1111, 0b1000, 0b1000, 0b1111, 0b0001, 0b0001, 0b1111},
        /* 0 1 2 3
        **********
        0| A A A A
        1| A
        2| A
        3| A A A A
        4|       A
        5|       A
        6| A A A A
        **********/
        {0b1111, 0b1000, 0b1000, 0b1111, 0b1001, 0b1001, 0b1111},
        /* 0 1 2 3
        **********
        0| A A A A
        1| A
        2| A
        3| A A A A
        4| A     A
        5| A     A
        6| A A A A
        **********/
        {0b1111, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001},
        /* 0 1 2 3
        **********
        0| A A A A
        1|       A
        2|       A
        3|       A
        4|       A
        5|       A
        6|       A
        **********/
        {0b1111, 0b1001, 0b1001, 0b1111, 0b1001, 0b1001, 0b1111},
        /* 0 1 2 3
        **********
        0| A A A A
        1| A     A
        2| A     A
        3| A A A A
        4| A     A
        5| A     A
        6| A A A A
        **********/
        {0b1111, 0b1001, 0b1001, 0b1111, 0b0001, 0b0001, 0b1111}
        /* 0 1 2 3
        **********
        0| A A A A
        1| A     A
        2| A     A
        3| A A A A
        4|       A
        5|       A
        6| A A A A
        **********/
};

int main()
{
    system("cls");
    printf("\033[?25l"); // hide cursor
    while (!_kbhit())
    {
        getTime();
        saveTime2Matrix();
        printf("%s\n\n\nPress any key to exit...\n", (const char *)matrix);
        printf("\033[0;0H"); // move cursor to (0,0)
    }
    system("cls");
    printf("\033[?25h"); // show cursor
}