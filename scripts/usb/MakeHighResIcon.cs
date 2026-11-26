using System;
using System.IO;
using System.Drawing;
using System.Drawing.Drawing2D;

class MakeHighResIcon
{
    static Bitmap DrawOrb(int size)
    {
        Bitmap bmp = new Bitmap(size, size);
        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.InterpolationMode = InterpolationMode.HighQualityBicubic;
            g.PixelOffsetMode = PixelOffsetMode.HighQuality;
            g.Clear(Color.Transparent);

            float center = size / 2f;
            float maxR = size * 0.46f;

            // 1. Ambient Glow
            for (float r = maxR; r >= maxR * 0.6f; r -= size * 0.04f)
            {
                int alpha = (int)(25 + (maxR - r) * 1.5f);
                if (alpha > 90) alpha = 90;
                using (SolidBrush b = new SolidBrush(Color.FromArgb(alpha, 0, 212, 255)))
                {
                    g.FillEllipse(b, center - r, center - r, r * 2, r * 2);
                }
            }

            // 2. Core Sphere with Gradient
            using (GraphicsPath path = new GraphicsPath())
            {
                float coreR = maxR * 0.72f;
                path.AddEllipse(center - coreR, center - coreR, coreR * 2, coreR * 2);
                using (PathGradientBrush pgb = new PathGradientBrush(path))
                {
                    pgb.CenterColor = Color.FromArgb(255, 255, 255, 255);
                    pgb.CenterPoint = new PointF(center - coreR * 0.25f, center - coreR * 0.25f);
                    pgb.SurroundColors = new Color[] { Color.FromArgb(240, 0, 160, 255) };
                    g.FillPath(pgb, path);
                }
            }

            // 3. Purple Flare Ring
            float flareR = maxR * 0.55f;
            using (SolidBrush b = new SolidBrush(Color.FromArgb(170, 155, 89, 247)))
            {
                g.FillEllipse(b, center - flareR * 0.7f, center - flareR * 0.7f, flareR * 1.4f, flareR * 1.4f);
            }

            // 4. White Hot Center Specular
            float hotR = maxR * 0.22f;
            using (SolidBrush b = new SolidBrush(Color.FromArgb(255, 255, 255, 255)))
            {
                g.FillEllipse(b, center - hotR - (size * 0.05f), center - hotR - (size * 0.05f), hotR * 2, hotR * 2);
            }
        }
        return bmp;
    }

    static void Main()
    {
        int[] sizes = new int[] { 256, 128, 64, 48, 32, 16 };
        byte[][] pngData = new byte[sizes.Length][];

        for (int i = 0; i < sizes.Length; i++)
        {
            using (Bitmap b = DrawOrb(sizes[i]))
            {
                using (MemoryStream ms = new MemoryStream())
                {
                    b.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
                    pngData[i] = ms.ToArray();
                }
            }
        }

        string icoPath = @"C:\Users\incey\.gemini\antigravity\scratch\ai-os\scripts\usb\ai_os.ico";
        using (FileStream fs = new FileStream(icoPath, FileMode.Create))
        using (BinaryWriter bw = new BinaryWriter(fs))
        {
            // ICONHEADER
            bw.Write((ushort)0); // reserved
            bw.Write((ushort)1); // type 1 = icon
            bw.Write((ushort)sizes.Length); // count

            int offset = 6 + (16 * sizes.Length);

            // ICONDIRENTRY array
            for (int i = 0; i < sizes.Length; i++)
            {
                bw.Write((byte)(sizes[i] >= 256 ? 0 : sizes[i])); // width
                bw.Write((byte)(sizes[i] >= 256 ? 0 : sizes[i])); // height
                bw.Write((byte)0); // colors
                bw.Write((byte)0); // reserved
                bw.Write((ushort)1); // planes
                bw.Write((ushort)32); // bpp
                bw.Write((uint)pngData[i].Length); // size
                bw.Write((uint)offset); // offset
                offset += pngData[i].Length;
            }

            // Write PNG image bytes
            for (int i = 0; i < sizes.Length; i++)
            {
                bw.Write(pngData[i]);
            }
        }

        Console.WriteLine("HIGH_RES_ICO_CREATED:" + icoPath);
    }
}
