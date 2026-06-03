import os
import shutil
import sys
import subprocess

def install_dependencies():
    print("Verificando dependências necessárias...")
    try:
        import pillow_heif
        from PIL import Image
        print("Dependências já estão instaladas!")
    except ImportError:
        print("Instalando pillow e pillow-heif para suportar arquivos HEIC...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "pillow-heif"])
            print("Dependências instaladas com sucesso!")
        except Exception as e:
            print(f"Erro ao instalar dependências: {e}")
            print("Por favor, execute manualmente: pip install pillow pillow-heif")
            sys.exit(1)

def convert_and_rename():
    from PIL import Image
    import pillow_heif
    pillow_heif.register_heif_opener()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, "imagens")
    backup_dir = os.path.join(img_dir, "originais")

    if not os.path.exists(img_dir):
        print(f"Erro: A pasta 'imagens' não foi encontrada em {img_dir}")
        return

    # Criar pasta de backup se não existir
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Listar arquivos, ignorando a pasta de backup e arquivos que já são fotoX.jpg
    files = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    
    # Ordenar arquivos para manter alguma consistência cronológica se possível
    files.sort()

    print(f"Encontrados {len(files)} arquivos para processar na pasta 'imagens'.")

    sucesso = 0
    for idx, filename in enumerate(files, 1):
        old_path = os.path.join(img_dir, filename)
        new_filename = f"foto{idx}.jpg"
        new_path = os.path.join(img_dir, new_filename)

        ext = os.path.splitext(filename)[1].lower()

        print(f"[{idx}/{len(files)}] Processando '{filename}'...")

        try:
            if ext == '.heic':
                # Converter HEIC para JPG
                image = Image.open(old_path)
                image.save(new_path, "JPEG", quality=90)
                # Mover o HEIC original para a pasta de backup
                shutil.move(old_path, os.path.join(backup_dir, filename))
                print(f"  -> Convertido e salvo como '{new_filename}' (Original movido para 'imagens/originais/')")
                sucesso += 1
            else:
                # Copiar/Mover JPG existente para o novo nome sequencial
                # Se já for um arquivo no formato fotoX.jpg, podemos pular ou processar.
                # Como listamos ignorando pastas, movemos o original para o backup e salvamos a cópia
                shutil.copy2(old_path, new_path)
                shutil.move(old_path, os.path.join(backup_dir, filename))
                print(f"  -> Renomeado para '{new_filename}' (Original movido para 'imagens/originais/')")
                sucesso += 1
        except Exception as e:
            print(f"  [ERRO] Falha ao processar {filename}: {e}")

    print(f"\nConcluído! {sucesso} de {len(files)} fotos foram processadas com sucesso.")
    print("Agora todas as suas fotos estão salvas como foto1.jpg, foto2.jpg ... foto37.jpg na pasta 'imagens'.")
    print("Os arquivos originais foram guardados com segurança na pasta 'imagens/originais/'.")

if __name__ == "__main__":
    install_dependencies()
    convert_and_rename()
