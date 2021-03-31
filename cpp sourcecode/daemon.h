#include <windows.h>

class daemon {
private:
	HWND Stealth;

public:
	void activate();

};

void daemon::activate()
{
		AllocConsole();
		Stealth = FindWindowA("ConsoleWindowClass", NULL);
		ShowWindow(Stealth, 0);

}