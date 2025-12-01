from rest_framework import serializers
from .models import Planta
from sala.models import Sala
from cadeira.models import Cadeira
import json

class PontosField(serializers.Field):
    """
    Campo customizado que aceita string JSON ou lista de pontos.
    Cada ponto representa uma Cadeira no sistema, com posições x e y (em porcentagem).
    """
    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Pontos devem ser uma string JSON válida ou lista")
        elif isinstance(data, list):
            return data
        elif data is None:
            return []
        else:
            raise serializers.ValidationError("Pontos devem ser uma string JSON ou lista")
    
    def to_representation(self, value):
        return value if value else []

class PlantaSerializer(serializers.ModelSerializer):
    pontos = PontosField(
        write_only=True,
        required=False,
        help_text="Lista de pontos onde cada ponto = uma Cadeira. Cada ponto deve ter {x, y} em porcentagem (0-100). Pode ser string JSON ou lista."
    )
    
    class Meta:
        model = Planta
        fields = ['id_planta', 'cadastro', 'nome', 'mapa_imagem', 'pontos']
        read_only_fields = ['id_planta', 'cadastro']
    
    def validate(self, data):
        """Validar dados antes de salvar"""
        print("🔍 VALIDANDO DADOS DO SERIALIZER")
        print(f"   Nome: {data.get('nome')}")
        print(f"   Imagem: {data.get('mapa_imagem')}")
        
        # Pontos já foi convertido pelo PontosField customizado
        # Cada ponto será convertido em uma Cadeira no banco
        if 'pontos' in data:
            pontos = data.get('pontos', [])
            if not isinstance(pontos, list):
                data['pontos'] = []
            print(f"   Pontos (cadeiras): {len(pontos)} pontos recebidos")
        
        return data
    
    def create(self, validated_data):
        print("\n" + "-"*70)
        print("🆕 SERIALIZER: CRIANDO NOVA PLANTA")
        print("-"*70)
        
        # Extrair pontos (pode não existir se não foi enviado)
        pontos_raw = validated_data.pop('pontos', None)
        
        # Inicializar pontos como lista vazia se não fornecido
        if pontos_raw is None:
            pontos = []
            print("ℹ️ Nenhum ponto fornecido, usando lista vazia")
        elif isinstance(pontos_raw, str):
            print(f"📝 Pontos recebidos como string, convertendo JSON...")
            try:
                pontos = json.loads(pontos_raw)
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao fazer parse dos pontos: {e}")
                pontos = []
        else:
            pontos = pontos_raw if pontos_raw else []
        
        print(f"📊 DADOS VALIDADOS:")
        print(f"   Nome: {validated_data.get('nome')}")
        cadastro = validated_data.get('cadastro')
        print(f"   Cadastro: {cadastro.id if cadastro else 'Será definido em perform_create'}")
        print(f"   Imagem: {validated_data.get('mapa_imagem')}")
        print(f"   Pontos (cadeiras): {len(pontos)} pontos = {len(pontos)} cadeiras")
        
        if pontos:
            print(f"   📍 Detalhamento dos pontos (cada um será uma cadeira):")
            for i, ponto in enumerate(pontos, 1):
                print(f"      Cadeira {i}: x={ponto.get('x', 0)}%, y={ponto.get('y', 0)}%")
        
        print("\n💾 SALVANDO PLANTA NO BANCO...")
        planta = super().create(validated_data)
        print(f"✅ Planta salva! ID: {planta.id_planta}")
        print(f"   Nome: {planta.nome}")
        
        # Verificar se a imagem foi salva
        if planta.mapa_imagem:
            print(f"   📎 Imagem salva em: {planta.mapa_imagem.path}")
            print(f"   🔗 URL da imagem: {planta.mapa_imagem.url}")
        else:
            print(f"   ⚠️  Nenhuma imagem fornecida")
        
        print("\n🏢 CRIANDO SALA PARA A PLANTA...")
        # Criar uma sala padrão para a planta
        sala, created = Sala.objects.get_or_create(
            planta=planta,
            defaults={
                'nome_sala': f'Sala Principal - {planta.nome}',
                'tipo': 'estacao',
                'capacidade': len(pontos) or 100,
                'descricao': f'Sala principal da planta {planta.nome}',
            }
        )
        
        if created:
            print(f"✅ Nova sala criada! ID: {sala.id_sala}")
        else:
            print(f"ℹ️  Sala já existia! ID: {sala.id_sala}")
        
        print(f"   Nome da sala: {sala.nome_sala}")
        print(f"   Capacidade: {sala.capacidade}")
        
        # Criar cadeiras baseadas nos pontos
        # IMPORTANTE: Cada ponto = uma Cadeira no banco de dados
        if pontos:
            print(f"\n🪑 CRIANDO {len(pontos)} CADEIRAS (um ponto = uma cadeira)...")
            # Ordenar pontos para garantir ordem consistente (por Y, depois X)
            pontos_ordenados = sorted(pontos, key=lambda p: (p.get('y', 0), p.get('x', 0)))
            
            cadeiras_criadas = []
            for i, ponto in enumerate(pontos_ordenados, 1):
                # Criar uma Cadeira para cada ponto
                cadeira = Cadeira.objects.create(
                    sala=sala,
                    pos_x=ponto.get('x', 0),  # Posição X em porcentagem (0-100)
                    pos_y=ponto.get('y', 0),  # Posição Y em porcentagem (0-100)
                    status='desocupada'        # Status inicial: desocupada
                )
                cadeiras_criadas.append(cadeira)
                # Nota: id_cadeira é único no banco, mas frontend usa IDs sequenciais (1, 2, 3...)
                print(f"   ✅ Cadeira {i}/{len(pontos_ordenados)} criada - ID banco: {cadeira.id_cadeira}, posição: ({cadeira.pos_x}%, {cadeira.pos_y}%)")
            print(f"✅ Total de {len(cadeiras_criadas)} cadeiras criadas a partir dos pontos!")
        else:
            print(f"ℹ️  Nenhum ponto fornecido, nenhuma cadeira será criada")
        
        print("-"*70 + "\n")
        return planta
    
    def update(self, instance, validated_data):
        print("\n" + "-"*70)
        print("✏️  SERIALIZER: ATUALIZANDO PLANTA")
        print("-"*70)
        print(f"🆔 Planta ID: {instance.id_planta}")
        print(f"📝 Nome atual: {instance.nome}")
        print(f"📝 Nome novo: {validated_data.get('nome', instance.nome)}")
        
        # Extrair pontos (já convertidos pelo PontosField)
        pontos = validated_data.pop('pontos', None)
        
        # Garantir que é uma lista ou None
        if pontos is not None:
            if not isinstance(pontos, list):
                pontos = []
                print("⚠️ Pontos não são uma lista, usando lista vazia")
            else:
                print(f"📍 {len(pontos)} pontos = {len(pontos)} cadeiras para atualizar")
                for i, p in enumerate(pontos, 1):
                    print(f"   Cadeira {i}: x={p.get('x')}%, y={p.get('y')}%")
        else:
            print(f"ℹ️  Nenhum ponto fornecido, mantendo cadeiras existentes")
        
        # Verificar imagem
        imagem_antiga = instance.mapa_imagem.name if instance.mapa_imagem else None
        if 'mapa_imagem' in validated_data:
            print(f"📎 Nova imagem fornecida: {validated_data['mapa_imagem'].name}")
        else:
            print(f"📎 Mantendo imagem atual: {imagem_antiga or 'Nenhuma'}")
        
        print("\n💾 ATUALIZANDO DADOS DA PLANTA...")
        # Atualizar dados da planta
        instance.nome = validated_data.get('nome', instance.nome)
        if 'mapa_imagem' in validated_data:
            print(f"   Substituindo imagem: {imagem_antiga} → {validated_data['mapa_imagem'].name}")
            instance.mapa_imagem = validated_data['mapa_imagem']
        instance.save()
        print(f"✅ Planta atualizada!")
        
        # Se pontos foram fornecidos, atualizar cadeiras
        # IMPORTANTE: Cada ponto = uma Cadeira no banco de dados
        if pontos is not None:
            print(f"\n🔄 ATUALIZANDO CADEIRAS (cada ponto = uma cadeira)...")
            # Buscar primeira sala ou criar uma nova
            sala = instance.salas.first()
            if not sala:
                print(f"   ⚠️  Nenhuma sala encontrada, criando nova sala...")
                sala = Sala.objects.create(
                    planta=instance,
                    nome_sala=f'Sala Principal - {instance.nome}',
                    tipo='estacao',
                    capacidade=len(pontos) or 100,
                    descricao=f'Sala principal da planta {instance.nome}',
                )
                print(f"✅ Nova sala criada! ID: {sala.id_sala}")
            else:
                print(f"   🏢 Sala encontrada: ID {sala.id_sala} - {sala.nome_sala}")
                # Verificar cadeiras existentes
                cadeiras_antigas = sala.cadeiras.count()
                print(f"   🪑 Cadeiras existentes: {cadeiras_antigas}")
                
                # Atualizar capacidade se necessário
                if len(pontos) > sala.capacidade:
                    print(f"   📈 Aumentando capacidade: {sala.capacidade} → {len(pontos)}")
                    sala.capacidade = len(pontos)
                    sala.save()
            
            # Deletar cadeiras antigas
            cadeiras_deletadas = sala.cadeiras.all().delete()[0]
            print(f"   🗑️  {cadeiras_deletadas} cadeiras antigas deletadas")
            
            # Criar novas cadeiras (um ponto = uma cadeira)
            print(f"   🆕 Criando {len(pontos)} novas cadeiras (um ponto = uma cadeira)...")
            for i, ponto in enumerate(pontos, 1):
                # Cada ponto vira uma Cadeira no banco
                cadeira = Cadeira.objects.create(
                    sala=sala,
                    pos_x=ponto.get('x', 0),  # Posição X em porcentagem
                    pos_y=ponto.get('y', 0),  # Posição Y em porcentagem
                    status='desocupada'        # Status inicial: desocupada
                )
                print(f"      ✅ Cadeira {i}/{len(pontos)} criada - ID banco: {cadeira.id_cadeira}, pos: ({cadeira.pos_x}%, {cadeira.pos_y}%)")
            print(f"✅ Total de {len(pontos)} cadeiras criadas a partir dos pontos!")
        
        print("-"*70 + "\n")
        return instance
    
    def to_representation(self, instance):
        """Inclui os pontos (cadeiras) na resposta"""
        print("📤 SERIALIZER: Montando resposta para envio")
        
        data = super().to_representation(instance)
        
        # Se mapa_imagem existe, garantir que seja apenas o caminho relativo
        if data.get('mapa_imagem'):
            # Remover URL completa se houver, deixar apenas o caminho
            mapa_imagem = data['mapa_imagem']
            if mapa_imagem.startswith('http://') or mapa_imagem.startswith('https://'):
                # Extrair apenas o caminho
                from urllib.parse import urlparse
                parsed = urlparse(mapa_imagem)
                data['mapa_imagem'] = parsed.path
                print(f"   📎 URL da imagem normalizada: {data['mapa_imagem']}")
        
        # Buscar cadeiras da sala principal e converter em pontos
        # IMPORTANTE: Cada Cadeira no banco = um ponto na resposta
        try:
            sala = instance.salas.first()
            if sala:
                cadeiras = sala.cadeiras.all().order_by('id_cadeira')  # Ordenar para consistência
                # Converter cadeiras em pontos (cada cadeira = um ponto)
                # Retornar IDs sequenciais começando do 1 para cada planta (não usar id_cadeira do banco)
                data['pontos'] = [
                    {
                        'id': index + 1,  # ID sequencial começando do 1 para esta planta
                        'x': cadeira.pos_x,  # Posição X da cadeira em porcentagem
                        'y': cadeira.pos_y   # Posição Y da cadeira em porcentagem
                    }
                    for index, cadeira in enumerate(cadeiras)
                ]
                print(f"   📍 Incluindo {len(data['pontos'])} pontos (cadeiras) na resposta (IDs resetados: 1-{len(data['pontos'])})")
            else:
                data['pontos'] = []
                print(f"   ⚠️  Nenhuma sala encontrada, pontos vazios")
        except Exception as e:
            data['pontos'] = []
            print(f"   ❌ Erro ao buscar pontos: {str(e)}")
        
        print(f"✅ Resposta montada: ID={data.get('id_planta')}, Nome={data.get('nome')}, Pontos={len(data.get('pontos', []))}")
        return data