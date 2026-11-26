using System;
using System.IO;
using System.Drawing;
using System.Drawing.Drawing2D;

class MakeIcon
{
    static void Main()
    {
        using (Bitmap bmp = new Bitmap(256, 256))
        {
            using (Graphics g = Graphics.FromImage(bmp))
            {
                g.SmoothingMode = SmoothingMode.AntiAlias;
                g.Clear(Color.Transparent);

                // Outer Glow layers
                for (int r = 120; r >= 70; r -= 10)
                {
                    int alpha = 18 + (120 - r) * 2;
                    using (SolidBrush b = new SolidBrush(Color.FromArgb(alpha, 0, 212, 255)))
                    {
                        g.FillEllipse(b, 128 - r, 128 - r, r * 2, r * 2);
                    }
                }

                // Core Gradient steps
                using (SolidBrush b1 = new SolidBrush(Color.FromArgb(235, 0, 180, 255)))
                {
                    g.FillEllipse(b1, 128 - 60, 128 - 60, 120, 120);
                }
                using (SolidBrush b2 = new SolidBrush(Color.FromArgb(245, 155, 89, 247)))
                {
                    g.FillEllipse(b2, 128 - 42, 128 - 42, 84, 84);
                }
                using (SolidBrush b3 = new SolidBrush(Color.FromArgb(255, 255, 255, 255)))
                {
                    g.FillEllipse(b3, 128 - 22, 128 - 22, 44, 44);
                }
            }

            IntPtr hIcon = bmp.GetHicon();
            using (Icon icon = Icon.FromHandle(hIcon))
            {
                string outPath = @"C:\Users\incey\.gemini\antigravity\scratch\ai-os\scripts\usb\ai_os.ico";
                using (FileStream fs = new FileStream(outPath, FileMode.Create))
                {
                    icon.Save(fs);
                }
                Console.WriteLine("SUCCESS:" + outPath);
            }
        }
    }
}
