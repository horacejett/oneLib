// src/features/chat-config/components/IconUploadSection.tsx
import Avator from "@/components/onelib-ui/input/avator";
import { Label } from "@/components/onelib-ui/label";
import { useToast } from "@/components/onelib-ui/toast/use-toast";
import { uploadFileWithProgress } from "@/modals/UploadModal/upload";
import Compressor from "compressorjs";
import { Plus } from "lucide-react";
import { useTranslation } from "react-i18next";

const MaxFileSize = 999 * 1024 * 1024; // 999MB

const toAssetUrl = (url?: string) => {
    if (!url) return '';
    if (/^(https?:)?\/\//.test(url) || url.startsWith('data:') || url.startsWith('blob:')) return url;

    const baseUrl = __APP_ENV__.BASE_URL || '';
    if (!baseUrl || baseUrl === '/') return url;

    return `${baseUrl.replace(/\/$/, '')}/${url.replace(/^\//, '')}`;
};

export const IconUploadSection = ({
    label,
    enabled,
    image,
    onToggle,
    onUpload,
}: {
    label: string;
    enabled: boolean;
    image: string;
    onToggle: (enabled: boolean) => void;
    onUpload: (url: string, relative_path?: string) => void;
}) => {

    const { toast } = useToast();
    const { t } = useTranslation();

    const handleFileChange = async (file: File | null) => {
        if (!file) return onUpload('', '');

        new Compressor(file, {
            quality: 0.6, // Compression quality (0-1)
            maxWidth: 300,
            maxHeight: 300,
            success(result) {
                // Compressed file (result is a Blob type)
                const compressedFile = new File([result], file.name, { type: result.type });
                uploadFileWithProgress(compressedFile, (progress) => { }, 'icon', '').then(res => {
                    if (!res?.file_path) {
                        toast({
                            title: t('chat.uploadFailedCheckFormat'),
                            variant: 'error'
                        });
                        return;
                    }
                    onUpload(res.file_path, res.relative_path || '')
                });
            },
            error(err) {
                console.error("Compression failed:", err);
                toast({
                    title: t('chat.uploadFailedCheckFormat'),
                    description: err.message,
                    variant: 'error'
                })
            },
        });
    }

    return <div>
        <div className="flex items-center gap-4">
            <Label className="onelib-label">{label}</Label>
            {/* <Switch checked={enabled} onCheckedChange={onToggle} /> */}
        </div>
        <Avator
            value={toAssetUrl(image)}
            size={MaxFileSize}
            close
            className="mt-3"
            onChange={handleFileChange}
            accept="image/png,image/jpeg"
        >
            <div className="size-28 rounded-sm border flex items-center justify-center">
                <Plus />
            </div>
        </Avator>
    </div>
};
