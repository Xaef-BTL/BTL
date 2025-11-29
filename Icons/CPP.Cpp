#include <windows.h>
#include <gdiplus.h>
#include <vector>
#include <string>
#include <algorithm>

#pragma comment (lib,"Gdiplus.lib")
using namespace Gdiplus;
using namespace std;

struct MiniWindow {
    HWND hwnd;
    int x, y, width, height;
    bool dragging;
    int offsetX, offsetY;
    wstring title;
};

struct Icon {
    int x, y;
    wstring label;
    HBITMAP bitmap;
};

vector<Icon> icons;
vector<MiniWindow> miniWindows;

bool startMenuOpen = false;
RECT startButtonRect = { 0,550,100,600 };

HBITMAP LoadPNGAsHBITMAP(const wchar_t* filename)
{
    Bitmap* bmp = new Bitmap(filename);
    HBITMAP hBmp;
    bmp->GetHBITMAP(Color::White, &hBmp);
    delete bmp;
    return hBmp;
}

void CreateMiniWindow(const wstring& title, int x, int y)
{
    MiniWindow mw;
    mw.x = x; mw.y = y; mw.width = 300; mw.height = 200;
    mw.dragging = false;
    mw.title = title;
    mw.hwnd = CreateWindowEx(0, L"STATIC", title.c_str(), WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        x, y, mw.width, mw.height, NULL, NULL, NULL, NULL);
    miniWindows.push_back(mw);
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
    case WM_PAINT:
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        Graphics graphics(hdc);

        // Masaüstü ikonları
        for (auto& icon : icons) {
            graphics.DrawImage(Image::FromHBITMAP(icon.bitmap, NULL), icon.x, icon.y, 64, 64);
            TextOutW(hdc, icon.x, icon.y + 66, icon.label.c_str(), icon.label.size());
        }

        // Başlat butonu
        graphics.FillRectangle(&SolidBrush(Color(200, 50, 50)), startButtonRect.left, startButtonRect.top, startButtonRect.right - startButtonRect.left, startButtonRect.bottom - startButtonRect.top);
        TextOutW(hdc, 10, 560, L"Başlat", 6);

        // Başlat menüsü
        if (startMenuOpen) {
            graphics.FillRectangle(&SolidBrush(Color(100, 100, 100)), 0, 450, 150, 550);
            TextOutW(hdc, 10, 460, L"Not Defteri", 10);
            TextOutW(hdc, 10, 480, L"Hesap Makinesi", 16);
        }

        EndPaint(hwnd, &ps);
    }
    break;

    case WM_LBUTTONDOWN:
    {
        int mx = GET_X_LPARAM(lParam);
        int my = GET_Y_LPARAM(lParam);

        // Başlat butonu tıklaması
        if (PtInRect(&startButtonRect, POINT{ (LONG)mx,(LONG)my })) {
            startMenuOpen = !startMenuOpen;
            InvalidateRect(hwnd, NULL, TRUE);
        }

        // İkon tıklaması
        for (auto& icon : icons) {
            if (mx >= icon.x && mx <= icon.x + 64 && my >= icon.y && my <= icon.y + 64) {
                CreateMiniWindow(icon.label, 100 + miniWindows.size() * 20, 100 + miniWindows.size() * 20);
            }
        }

    }
    break;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow)
{
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

    const wchar_t CLASS_NAME[] = L"UltraMiniPC";
    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(0, CLASS_NAME, L"Ultra Mini PC", WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);

    // Örnek ikonlar
    Icon notDefteri;
    notDefteri.x = 50; notDefteri.y = 50;
    notDefteri.label = L"Not Defteri";
    notDefteri.bitmap = LoadPNGAsHBITMAP(L"C:\\Users\\Yiğit Aslan\\Desktop\\notepad.png");
    icons.push_back(notDefteri);

    Icon hesap;
    hesap.x = 150; hesap.y = 50;
    hesap.label = L"Hesap Makinesi";
    hesap.bitmap = LoadPNGAsHBITMAP(L"C:\\Users\\Yiğit Aslan\\Desktop\\calculator.png");
    icons.push_back(hesap);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    GdiplusShutdown(gdiplusToken);
    return 0;
}
