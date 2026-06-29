import { Label } from "@/components/onelib-ui/label"
import { Switch } from "@/components/onelib-ui/switch"
import { QuestionTooltip } from "@/components/onelib-ui/tooltip"
import { useState } from "react"
import { useTranslation } from "react-i18next"

export default function SwitchItem({ data, onChange, i18nPrefix }) {
    const [value, setValue] = useState(data.value)
    const { t } = useTranslation('flow')

    return <div className='node-item mb-4 flex justify-between' data-key={data.key}>
        <Label className="flex items-center onelib-label">
            {t(`${i18nPrefix}label`)}
            {data.help && <QuestionTooltip content={t(`${i18nPrefix}help`)} />}
        </Label>
        <Switch checked={value} onCheckedChange={(bln) => {
            setValue(bln)
            onChange(bln)
        }} />
    </div>
};
